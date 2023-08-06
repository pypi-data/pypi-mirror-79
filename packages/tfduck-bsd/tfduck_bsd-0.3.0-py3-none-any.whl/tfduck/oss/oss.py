import oss2
import os
import uuid
import time
from django.conf import settings
from tfduck.common.defines import BMOBJ, Et
import base64
import pathlib
import threading
import gzip

class AliyunOss(object):
    """
    @des: 阿里云oss的基本操作
    """

    def __init__(self, bucket_name, aly_access_key_id, aly_access_key_secret, aly_endpoint):
        """
        @des:初始化
        """
        self.access_key_id = aly_access_key_id
        self.access_key_secret = aly_access_key_secret
        self.bucket_name = bucket_name
        # oss-us-east-1.aliyuncs.com
        self.endpoint = aly_endpoint
        self.bucket = oss2.Bucket(oss2.Auth(self.access_key_id, self.access_key_secret),
                                  self.endpoint, self.bucket_name)

    def gen_local_unique_file(self, ext="csv"):
        """
        @des:生成本地文件唯一路径
        """
        if BMOBJ.get_current_env() == "server":
            media_root = settings.MEDIA_ROOT
            base_dir = os.path.join(media_root, "data")
        else:
            base_dir = os.path.join(os.environ.get('HOME', ''), "tmp/tfduck")
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        real_name = "%s%s.%s" % (uuid.uuid1().hex, uuid.uuid1().hex, ext)
        file_path = os.path.join(base_dir, real_name)
        return file_path

    def download(self, remote_filename):
        """
        @des:下载oss文件到本地---head_object
        """
        BMOBJ.log_error("download", remote_filename,  "start")
        #
        unique_path = self.gen_local_unique_file()
        tmp_unique_file = "%s.tmp.json" % unique_path
        #
        total_retry = 18
        for i in range(total_retry):
            try:
                self.bucket.restore_object(remote_filename)
            except Exception as _:
                pass

            try:
                oss2.resumable_download(
                    self.bucket, remote_filename, tmp_unique_file)
                break
            except Exception as e:
                BMOBJ.remove_file(tmp_unique_file)
                if i >= total_retry-1:
                    raise e
                else:
                    time.sleep(10)
        os.rename(tmp_unique_file, unique_path)
        #
        BMOBJ.log_error("download", remote_filename,  "end")
        #
        if 0:
            with open(unique_path, 'rb') as f:
                file_content = f.read()
            BMOBJ.remove_file(unique_path)
            file_base64_str = base64.b64encode(file_content).decode()
            return file_base64_str
        else:
            with open(unique_path, 'r') as f:
                file_content = f.read()
            BMOBJ.remove_file(unique_path)
            #
            return file_content
        

    def upload(self, file_content, remote_filename):
        """
        @des:上传文件
        @param file_content: 字符串
        @param remote_filename: 上传到远程oss的路径
        """
        BMOBJ.log_error("upload",  "start")
        if type(file_content)!=str:
            raise Et(2, "file_content must be str")
        # local_filename = download_image_local(fid)
        unique_path = self.gen_local_unique_file()
        tmp_unique_file = "%s.tmp.json" % unique_path
        if 0:
            with open(tmp_unique_file, 'wb') as f:
                f.write(file_content)
        else:
            with open(tmp_unique_file, 'w') as f:
                f.write(file_content)
        os.rename(tmp_unique_file, unique_path)
        result = oss2.resumable_upload(
            self.bucket, remote_filename, unique_path)
        BMOBJ.remote_filename(unique_path)
        #
        BMOBJ.log_error(result)
        BMOBJ.log_error("upload",  "end")
        return True

    def exists(self, remote_filename):
        """
        @des: 判断oss上面文件是否存在
        """
        exists = self.bucket.object_exists(remote_filename)
        return exists
    
    def delete_path(self, remote_path):
        """
        废弃
        @des: 删除一个远程path，和下面所有的文件---废弃，用下面的delete_prefix_oss
        """
        for obj in oss2.ObjectIterator(self.bucket, prefix=remote_path, delimiter='/'):
            exist_file_path = obj.key
            self.bucket.delete_object(exist_file_path)
        return True
    
    def delete_prefix_oss(self, ctx, bucket, oss_file_path):
        """
        @des: 删除oss的文件夹
        """
        # 必须以/结尾
        if oss_file_path[-1] != "/":
            oss_file_path += "/"
        #
        for obj in oss2.ObjectIterator(bucket, prefix=oss_file_path, delimiter='/'):
            exist_file_path = obj.key
            bucket.delete_object(exist_file_path)

    def _download_oss(self, ctx, bucket, td_file, local_file):
        for i in range(3):  # 最多重试三次，由于网络不稳定等问题
            try:
                _s = time.time()
                result = bucket.get_object_to_file(td_file, local_file)
                _e = time.time()
                BMOBJ.clog(
                    ctx, f"{local_file} download status {result.status}, sub time {_e-_s}", )
                break
            except Exception as e:
                BMOBJ.clog(
                    ctx, f"{local_file} download oss fail, repeat {i}, error: {e}")
                continue

    def download_oss(self, ctx, bucket, local_file_path, oss_file_path):
        """
        @des: 下载到oss---多线程下载---下载文件夹--下载后删除oss的文件
        auth = oss2.Auth(self.oss_access_id_i, self.oss_access_key_i)
        bucket = oss2.Bucket(auth, self.oss_endpoint_i, self.oss_bucket_i)
        """
        s = time.time()
        # 删除本地已经存在的文件,重新创建本地路径
        BMOBJ.remove_folder(local_file_path)
        os.makedirs(local_file_path)
        # 下载
        subfiles = []
        for obj in oss2.ObjectIterator(bucket, prefix=oss_file_path, delimiter='/'):
            exist_file_path = obj.key
            subfiles.append(exist_file_path)
        if subfiles:
            tds = []
            for subfile in subfiles:
                td_file = subfile
                subfile_name = pathlib.PurePath(td_file).name
                local_file = f"{local_file_path}/{subfile_name}"
                t = threading.Thread(target=self._download_oss,
                                     args=(ctx, bucket, td_file, local_file))
                tds.append(t)
            for td in tds:
                # 表示该线程是不重要bai的,进程退出时不需要等待这个线程执行完成。
                # 这样做的意义在于：避免子线程无限死循环，导致退不出程序，也就是避免楼上说的孤儿进程。
                # thread.setDaemon（）设置为True, 则设为true的话 则主线程执行完毕后会将子线程回收掉,
                # 设置为false,主进程执行结束时不会回收子线程
                td.setDaemon(True)
                td.start()
            for td in tds:
                td.join()
        e = time.time()
        # 删除oss已经存在的part_date的文件---内网端
        self.delete_prefix_oss(ctx, bucket, oss_file_path)
        #
        BMOBJ.clog(
            ctx, f"{oss_file_path} download oss all time", e-s)

    def _upload_oss(self, ctx,  bucket, td_file, local_file):
        # BMOBJ.clog(ctx, f"sub upload start {td_file} {local_file}")
        for i in range(3):  # 最多重试三次，由于网络不稳定等问题
            try:
                _s = time.time()
                result = bucket.put_object_from_file(td_file, local_file)
                _e = time.time()
                BMOBJ.clog(
                    ctx, f"{local_file} upload status {result.status}, sub time {_e-_s}", )
                break
            except Exception as e:
                BMOBJ.clog(
                    ctx, f"{local_file} upload oss fail, repeat {i}, error: {e}")
                continue

    def upload_oss(self, ctx, bucket, local_file_path, oss_file_path, add_success=False, add_empty=False):
        """
        @des: 上传到oss---多线程上传---上传文件夹
        auth = oss2.Auth(self.oss_access_id, self.oss_access_key)
        bucket = oss2.Bucket(auth, self.oss_endpoint, self.oss_bucket)
        """
        s = time.time()
        # 删除oss已经存在的part_date的文件
        self.delete_prefix_oss(ctx, bucket, oss_file_path)
        # 上传
        subfiles = list(pathlib.Path(local_file_path).glob("*"))
        if subfiles:
            tds = []
            for subfile in subfiles:
                td_file = f'{oss_file_path}{subfile.name}'
                local_file = str(subfile)
                t = threading.Thread(target=self._upload_oss,
                                     args=(ctx, bucket, td_file, local_file))
                tds.append(t)
            for td in tds:
                # 表示该线程是不重要bai的,进程退出时不需要等待这个线程执行完成。
                # 这样做的意义在于：避免子线程无限死循环，导致退不出程序，也就是避免楼上说的孤儿进程。
                # thread.setDaemon（）设置为True, 则设为true的话 则主线程执行完毕后会将子线程回收掉,
                # 设置为false,主进程执行结束时不会回收子线程
                td.setDaemon(True)
                td.start()
            for td in tds:
                td.join()
            if add_success:
                # 上传成功后，上传一个空文件代表成功
                success_file = "/mydata/_SUCCESS"
                with gzip.open(success_file, 'wb') as r:
                    r.write(b'')
                self._upload_oss(
                    ctx, bucket, f'{oss_file_path}_SUCCESS', success_file)
        else:
            if add_empty:
                # 上传一个empty文件，代表没有数据
                empty_file = "/mydata/_EMPTY"
                with gzip.open(empty_file, 'wb') as r:
                    r.write(b'')
                self._upload_oss(
                    ctx, bucket, f'{oss_file_path}_EMPTY', empty_file)
        e = time.time()
        # 删除所有本地文件
        BMOBJ.remove_folder(local_file_path)
        #
        BMOBJ.clog(
            ctx, f"{oss_file_path} upload oss all time", e-s)

