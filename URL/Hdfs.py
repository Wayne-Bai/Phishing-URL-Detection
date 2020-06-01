import pyhdfs


class Hdfs():

    def __init__(self):
        self.fs = pyhdfs.HdfsClient('localhost:50070')

    # 删除
    def delFile(self, path):
        fs = self.fs
        fs.delete(path)

    # 上传文件
    def upload(self, fileName, tmpFile):
        fs = self.fs
        fs.copy_from_local(fileName, tmpFile)

    # 新建目录
    def makdir(self, filePath):
        fs = self.fs
        if not fs.exists(filePath):
            # os.system('hadoop fs -mkdir '+filePath)
            fs.mkdirs(filePath)
            return 'mkdir'
        return 'exits'

    # 重命名
    def rename(self, srcPath, dstPath):
        fs = self.fs
        if not fs.exists(srcPath):
            return
        fs.rename(srcPath, dstPath)

