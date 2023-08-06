from config import config as deepvac_config
import os
import sys
import numpy as np
import torch
import time
try:
    import faiss
except:
    LOG.W("Faiss not installed. You cannot use the API implemented based on Faiss library.")

from deepvac.syszux_report import ClassifierReport
from deepvac.syszux_log import LOG

def swigPtrFromTensor(x):
    """ gets a Faiss SWIG pointer from a pytorch trensor (on CPU or GPU) """
    assert x.is_contiguous()

    if x.dtype == torch.float32:
        return faiss.cast_integer_to_float_ptr(x.storage().data_ptr() + x.storage_offset() * 4)
    
    if x.dtype == torch.int64:
        return faiss.cast_integer_to_long_ptr(x.storage().data_ptr() + x.storage_offset() * 8)

    raise Exception("tensor type not supported: {}".format(x.dtype))

class FeatureVector(object):
    def __init__(self, deepvac_config):
        self.conf = deepvac_config
        assert self.conf.db_path_list, 'You must configure config.db_path_list in config.py'
        assert self.conf.map_locs, 'You must configure config.map_locs in config.py, which is to specify how mapping the feature to CUDA/CPU device'
        assert len(self.conf.map_locs) == len(self.conf.db_path_list), 'config.db_path_list number should be same with config.map_locs'
        self.dbs = []
        if not self.conf.name:
            self.conf.name = 'gemfield'

        if not self.conf.log_every:
            self.conf.log_every = 10000

    def loadDB(self):
        for db_path, map_loc in zip(self.conf.db_path_list, self.conf.map_locs):
            self.dbs.append(torch.load(db_path, map_location = map_loc))

    def searchDB(self, xb, xq, k=2):
        D = []
        I = []
        if k < 1 or k > 10:
            LOG.logE('illegal nearest neighbors parameter k(1 ~ 10): {}'.format(k))
            return D, I

        distance = torch.norm(xb - xq, dim=1)
        for i in range(k):
            values, indices = distance.kthvalue(i+1)
            D.append(values.item())
            I.append(indices.item())
        return D, I

    def searchAllDB(self, xq, k=2):
        raise Exception("Cannot do searchAllDB in base class, since no names can be used to re index feature accross multi DB BLOCK.")

    def printClassifierReport(self):
        pass

class NamesPathsClsFeatureVector(FeatureVector):
    def __init__(self, deepvac_config):
        super(NamesPathsClsFeatureVector, self).__init__(deepvac_config)
        assert self.conf.class_num, 'You must configure config.class_num in config.py'
        assert self.conf.np_path_list, 'You must configure config.np_path_list in config.py'
        assert len(self.conf.np_path_list) == len(self.conf.db_path_list), 'config.db_path_list number should be same with config.np_path_list'
        self.names = []
        self.paths = []

    def loadDB(self):
        super(NamesPathsClsFeatureVector, self).loadDB()
        for np_path in self.conf.np_path_list:
            npf = np.load(np_path)
            self.names.append(npf['names'])
            self.paths.append(npf['paths'])

    def searchAllDB(self, xq, k=2):
        TMP_D = []
        TMP_N = []
        for i, db in enumerate(self.dbs):
            xq = xq.to(db.device)
            distances, indices = self.searchDB(db, xq, k)
            TMP_D.extend(distances)
            TMP_N.extend(self.names[i][indices])

        N = [n for _,n in sorted(zip(TMP_D,TMP_N))]
        D = sorted(TMP_D)

        return D[:k], N[:k]

    def printClassifierReport(self):
        report = ClassifierReport(self.conf.name, self.conf.class_num, self.conf.class_num)
        for i, db in enumerate(self.dbs):
            name = self.names[i]
            path = self.paths[i]
            for idx, emb in enumerate(db):
                _, N = self.searchAllDB(emb)
                should_be_gt, pred = N[0], N[1]
                LOG.logI("label : {}".format(name[idx]))
                LOG.logI("pred : {}".format(pred))
                if idx % self.conf.log_every == 0:
                    LOG.logI("Process {} img...".format(idx))
                report.add(int(name[idx]), int(pred))
        report()

class NamesPathsClsFeatureVectorByFaiss(NamesPathsClsFeatureVector):
    def __init__(self, deepvac_config):
        super(NamesPathsClsFeatureVectorByFaiss, self).__init__(deepvac_config)
        if 'faiss' not in sys.modules:
            LOG.logE("Faiss not installed, cannot use this class.", exit=True)

    def loadDB(self):
        super(NamesPathsClsFeatureVectorByFaiss, self).loadDB()
        for db_path in self.conf.db_path_list:
            self.dbs.append(torch.load(db_path).to('cpu').numpy().astype('float32'))

    def searchAllDB(self, xq, k=2):
        D = []
        N = []
        d = self.dbs[0][0].shape[-1]
        LOG.logI('Load index start...')
        cpu_index = faiss.IndexFlatL2(d)
        gpu_index = faiss.index_cpu_to_all_gpus(cpu_index)
        LOG.logI('Load index finished...')
        
        for i, db in enumerate(self.dbs):
            name = self.names[i]
            gpu_index.reset()
            gpu_index.add(db)
            tempD, tempI = gpu_index.search(xq, k)
            tempN = name[tempI]

            if len(D) == 0:
                D, N = tempD, tempN
                continue
            D = np.hstack((D, tempD))
            N = np.hstack((N, tempN))

        RD, RN = D, N
        for i, d in enumerate(D):
            index = np.argsort(d)
            RD[i] = D[i][index]
            RN[i] = N[i][index]

        return RD[:, :k], RN[:, :k]

    def printClassifierReport(self):
        report = ClassifierReport(self.conf.name, self.conf.class_num, self.conf.class_num)
        for i, xq in enumerate(self.dbs):
            LOG.logI('Process {} db...'.format(i))
            name = self.names[i]
            path = self.paths[i]
            RD, RN = self.searchAllDB(xq)

            for idx, n in enumerate(RN):
                pred_ori, pred = n[0], n[1]
                LOG.logI("label : {}".format(name[idx]))
                LOG.logI("pred : {}".format(pred))
                if idx % self.conf.log_every == 0:
                    LOG.logI("Process {} img...".format(idx))
                report.add(int(name[idx]), int(pred))

        report()

class NamesPathsClsFeatureVectorByFaissPytorch(FeatureVectorByFaiss):
    def __init__(self, deepvac_config):
        super(NamesPathsClsFeatureVectorByFaissPytorch, self).__init__(deepvac_config)
        self.dbs = []
                           
    def loadDB(self):
        super(NamesPathsClsFeatureVectorByFaissPytorch, self).loadDB()
        assert self.conf.db_path_list, 'You must configure config.db_path_list in config.py'
        assert self.conf.map_locs, 'You must configure config.map_locs in config.py'
        for db_path, map_loc in zip(self.conf.db_path_list, self.conf.map_locs):
            self.dbs.append(torch.load(db_path, map_location = map_loc))

    def search_index_pytorch(self, index, x, k, D=None, I=None):
        """call the search function of an index with pytorch tensor I/O (CPU
            and GPU supported)"""
        assert x.is_contiguous()
        n, d = x.size()
        assert d == index.d
        
        if D is None:
            D = torch.empty((n, k), dtype=torch.float32, device=x.device)             
        else:                                        
            assert D.size() == (n, k)
        
        if I is None:
            I = torch.empty((n, k), dtype=torch.int64, device=x.device)             
        else:                                                           
            assert I.size() == (n, k)
        
        torch.cuda.synchronize()
        xptr = swigPtrFromTensor(x)
        Iptr = swigPtrFromTensor(I)
        Dptr = swigPtrFromTensor(D)
        index.search_c(n, xptr, k, Dptr, Iptr)
        torch.cuda.synchronize()
        
        return D, I

    def searchAllDB(self, xq, k=2):        
        D = []
        N = []
        d = 512
        LOG.logI('Load index start...')
        res = faiss.StandardGpuResources()
        gpu_index = faiss.GpuIndexFlatL2(res, d)
        LOG.logI('Load index finished...')

        for i, db in enumerate(self.dbs):
            name = self.names[i]
            gpu_index.reset()
            gpu_index.add(db.to('cpu').numpy().astype('float32'))
            tempD, tempI = self.search_index_pytorch(gpu_index, xq, k)
            tempD = tempD.to('cpu').numpy()
            tempI = tempI.to('cpu').numpy()
            tempN = name[tempI]
            
            if len(D) == 0:
                D, N = tempD, tempN
                continue

            D = np.hstack((D, tempD))
            N = np.hstack((N, tempN))
            
        RD, RN = D, N    
        for i, d in enumerate(D):
            index = np.argsort(d)
            RD[i] = D[i][index]
            RN[i] = N[i][index]
        
        return RD[:, :k], RN[:, :k]

    def printClassifierReport(self):        
        report = ClassifierReport(self.conf.name, self.conf.class_num, self.conf.class_num)
        for i, xq in enumerate(self.dbs):
            LOG.logI('Process {} db...'.format(i))
            name = self.names[i]
            path = self.paths[i]
            RD, RN = self.searchAllDB(xq)
            
            for idx, n in enumerate(RN):
                pred_ori, pred = n[0], n[1]
                LOG.logI("label : {}".format(name[idx]))
                LOG.logI("pred : {}".format(pred))
                if idx % self.conf.log_every == 0:
                    LOG.logI("Process {} img...".format(idx))
                
                report.add(int(name[idx]), int(pred))
        
        report()

if __name__ == "__main__":
    from config import config
    fv = NamesPathsClsFeatureVector(config)
    fv.printClassifierReport()

