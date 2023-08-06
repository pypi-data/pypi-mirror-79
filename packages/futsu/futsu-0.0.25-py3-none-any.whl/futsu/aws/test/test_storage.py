import unittest
from unittest import TestCase
import futsu.aws.s3 as fstorage
import futsu.fs as ffs
import futsu.storage as ffstorage
import tempfile
import os
#from google.cloud import storage as gcstorage
import time

class TestStorage(TestCase):

    def test_is_bucket_path(self):
        self.assertTrue(fstorage.is_bucket_path('s3://bucket'))
        self.assertTrue(fstorage.is_bucket_path('s3://bucket/'))

        self.assertFalse(fstorage.is_bucket_path('s3://bucket//'))
        self.assertFalse(fstorage.is_bucket_path('s3://bucket/asdf'))
        self.assertFalse(fstorage.is_bucket_path('s3://bucket/asdf/'))
        self.assertFalse(fstorage.is_bucket_path('s3://bucket/asdf/asdf'))

        self.assertFalse(fstorage.is_bucket_path('s://bucket'))
        self.assertFalse(fstorage.is_bucket_path('3://bucket'))
        self.assertFalse(fstorage.is_bucket_path('s3//bucket'))
        self.assertFalse(fstorage.is_bucket_path('s3:/bucket'))
        self.assertFalse(fstorage.is_bucket_path('s3://'))
        self.assertFalse(fstorage.is_bucket_path('s3:///'))
        self.assertFalse(fstorage.is_bucket_path('s3:///asdf'))

    def test_is_blob_path(self):
        self.assertFalse(fstorage.is_blob_path('s3://bucket'))
        self.assertFalse(fstorage.is_blob_path('s3://bucket/'))

        self.assertTrue(fstorage.is_blob_path('s3://bucket//'))
        self.assertTrue(fstorage.is_blob_path('s3://bucket/asdf'))
        self.assertTrue(fstorage.is_blob_path('s3://bucket/asdf/'))
        self.assertTrue(fstorage.is_blob_path('s3://bucket/asdf/asdf'))

        self.assertFalse(fstorage.is_blob_path('s://bucket'))
        self.assertFalse(fstorage.is_blob_path('3://bucket'))
        self.assertFalse(fstorage.is_blob_path('s3//bucket'))
        self.assertFalse(fstorage.is_blob_path('s3:/bucket'))
        self.assertFalse(fstorage.is_blob_path('s3://'))
        self.assertFalse(fstorage.is_blob_path('s3:///'))
        self.assertFalse(fstorage.is_blob_path('s3:///asdf'))

    def test_is_path(self):
        self.assertTrue(fstorage.is_path('s3://bucket'))
        self.assertTrue(fstorage.is_path('s3://bucket/'))

        self.assertTrue(fstorage.is_path('s3://bucket//'))
        self.assertTrue(fstorage.is_path('s3://bucket/asdf'))
        self.assertTrue(fstorage.is_path('s3://bucket/asdf/'))
        self.assertTrue(fstorage.is_path('s3://bucket/asdf/asdf'))

        self.assertFalse(fstorage.is_path('s://bucket'))
        self.assertFalse(fstorage.is_path('3://bucket'))
        self.assertFalse(fstorage.is_path('s3//bucket'))
        self.assertFalse(fstorage.is_path('s3:/bucket'))
        self.assertFalse(fstorage.is_path('s3://'))
        self.assertFalse(fstorage.is_path('s3:///'))
        self.assertFalse(fstorage.is_path('s3:///asdf'))

    def test_parse_bucket_path(self):
        self.assertEqual(fstorage.prase_bucket_path('s3://asdf'),'asdf')
        self.assertRaises(ValueError,fstorage.prase_bucket_path,'asdf')

    def test_prase_blob_path(self):
        self.assertEqual(fstorage.prase_blob_path('s3://asdf/qwer'),('asdf','qwer'))
        self.assertEqual(fstorage.prase_blob_path('s3://asdf/qwer/'),('asdf','qwer/'))
        self.assertRaises(ValueError,fstorage.prase_blob_path,'asdf')

    def test_gcp_string(self):
        timestamp = int(time.time())
        tmp_gs_path  = 's3://futsu-test/test-PPCFADJEPR-{0}'.format(timestamp)

        client = fstorage.create_client()
        fstorage.string_to_blob(tmp_gs_path,'NSODRIGNUR',client)
        s = fstorage.blob_to_string(tmp_gs_path,client)
        self.assertEqual(s,'NSODRIGNUR')

    def test_gcp_file(self):
        client = fstorage.create_client()
        with tempfile.TemporaryDirectory() as tempdir:
            timestamp = int(time.time())
            src_fn = os.path.join('futsu','gcp','test','test_storage.txt')
            tmp_gs_path  = 's3://futsu-test/test-TOPTSPZHLZ-{0}'.format(timestamp)
            tmp_filename = os.path.join(tempdir,'QDVBADVVVW')
            
            fstorage.file_to_blob(tmp_gs_path,src_fn,client)
            fstorage.blob_to_file(tmp_filename,tmp_gs_path,client)
            
            self.assertFalse(ffs.diff(src_fn,tmp_filename))

    def test_exist(self):
        timestamp = int(time.time())
        tmp_gs_path  = 's3://futsu-test/test-YYAZXVHGVW-{0}'.format(timestamp)

        client = fstorage.create_client()
        self.assertFalse(fstorage.is_blob_exist(tmp_gs_path,client))
        fstorage.string_to_blob(tmp_gs_path,'EYKVKUAUNU',client)
        self.assertTrue(fstorage.is_blob_exist(tmp_gs_path,client))

    def test_delete(self):
        timestamp = int(time.time())
        tmp_gs_path  = 's3://futsu-test/test-WABWGQVWRP-{0}'.format(timestamp)

        client = fstorage.create_client()

        self.assertFalse(fstorage.is_blob_exist(tmp_gs_path,client))

        fstorage.blob_rm(tmp_gs_path,client)

        self.assertFalse(fstorage.is_blob_exist(tmp_gs_path,client))

        fstorage.string_to_blob(tmp_gs_path,'RPUBYBJZSN',client)
        self.assertTrue(fstorage.is_blob_exist(tmp_gs_path,client))

        fstorage.blob_rm(tmp_gs_path,client)

        self.assertFalse(fstorage.is_blob_exist(tmp_gs_path,client))

    def test_acl(self):
        client = fstorage.create_client()
        with tempfile.TemporaryDirectory() as tempdir:
            timestamp = int(time.time())
            src_fn = os.path.join('futsu','gcp','test','test_storage.txt')
            tmp_gs_path  = 's3://futsu-test/test-TOPTSPZHLZ-{0}'.format(timestamp)
            tmp_http_path  = 'https://futsu-test.s3-us-west-2.amazonaws.com/test-TOPTSPZHLZ-{0}'.format(timestamp)
            tmp_filename = os.path.join(tempdir,'QHDCXHYRKZ')
            
            client = fstorage.create_client()

            # no upload, should be 404
            with self.assertRaises(Exception):
                blob_to_file(tmp_filename,tmp_http_path,client)

            # upload
            fstorage.file_to_blob(tmp_gs_path,src_fn,client)
            
            # bad acl, should be 403
            with self.assertRaises(Exception):
                ffstorage.path_to_local(tmp_filename,tmp_http_path)
            
            # set acl
            fstorage.set_blob_acl(tmp_gs_path, 'public-read', client)
            
            # should run ok
            ffstorage.path_to_local(tmp_filename,tmp_http_path)
            self.assertFalse(ffs.diff(src_fn,tmp_filename))

    def test_find_blob_itr(self):
        client = fstorage.create_client()
        timestamp = int(time.time())
        tmp_gs_path_list = ['s3://futsu-test/test-JJLVOWMQ-{0}/{1}'.format(timestamp,i) for i in range(10)]
        for tmp_gs_path in tmp_gs_path_list:
            fstorage.bytes_to_blob(tmp_gs_path,b'ZPMSMMAU',client)

        blob_list = fstorage.find_blob_itr('s3://futsu-test/test-JJLVOWMQ-{0}/'.format(timestamp), client)
        blob_list = list(blob_list)
        self.assertEqual(len(blob_list), 10)
        blob_list = sorted(blob_list)
        self.assertEqual(blob_list, tmp_gs_path_list)

        blob_list = fstorage.find_blob_itr('s3://futsu-test/test-JJLVOWMQ-{0}/'.format(timestamp), client, MaxKeys=5)
        blob_list = list(blob_list)
        self.assertEqual(len(blob_list), 10)
        blob_list = sorted(blob_list)
        self.assertEqual(blob_list, tmp_gs_path_list)

        blob_list = fstorage.find_blob_itr('s3://futsu-test/test-JJLVOWMQ-{0}/'.format(timestamp), client, MaxKeys=20)
        blob_list = list(blob_list)
        self.assertEqual(len(blob_list), 10)
        blob_list = sorted(blob_list)
        self.assertEqual(blob_list, tmp_gs_path_list)

        blob_list = fstorage.find_blob_itr('s3://futsu-test/test-HPYHCAMK-{0}/'.format(timestamp), client)
        blob_list = list(blob_list)
        self.assertEqual(len(blob_list), 0)

    def test_join(self):
        self.assertEqual(fstorage.join('s3://NARNEHCQ','UDGTMPFX'),'s3://NARNEHCQ/UDGTMPFX')
        self.assertEqual(fstorage.join('s3://NARNEHCQ','UDGTMPFX','AFOCASQL'),'s3://NARNEHCQ/UDGTMPFX/AFOCASQL')

    def test_split(self):
        self.assertEqual(fstorage.split('s3://NARNEHCQ/UDGTMPFX'),('s3://NARNEHCQ','UDGTMPFX'))
        self.assertEqual(fstorage.split('s3://NARNEHCQ/UDGTMPFX/AFOCASQL'),('s3://NARNEHCQ/UDGTMPFX','AFOCASQL'))

    def test_dirname(self):
        self.assertEqual(fstorage.dirname('s3://NARNEHCQ/UDGTMPFX'),'s3://NARNEHCQ')
        self.assertEqual(fstorage.dirname('s3://NARNEHCQ/UDGTMPFX/AFOCASQL'),'s3://NARNEHCQ/UDGTMPFX')

    def test_basename(self):
        self.assertEqual(fstorage.basename('s3://NARNEHCQ/UDGTMPFX'),'UDGTMPFX')
        self.assertEqual(fstorage.basename('s3://NARNEHCQ/UDGTMPFX/AFOCASQL'),'AFOCASQL')

    def test_rmtree(self):
        timestamp = int(time.time())
        path0 = f's3://futsu-test/test-HOSPFEUB-{timestamp}'
        path00 = fstorage.join(path0,'ITGDLUVB')
        path000 = fstorage.join(path00,'WKBXFDTH','CMCXBJYN')
        path001 = fstorage.join(path00,'MGNZJTXL','RGWIYPEG')
        path01  = fstorage.join(path0,'GMZSNRPD','UOAUKUKG','VJUOXIQY')
        path02 = fstorage.join(path0,'ITGDLUVBx')
        
        s3_client = fstorage.create_client()
        
        fstorage.bytes_to_blob(path000,b'',s3_client)
        fstorage.bytes_to_blob(path001,b'',s3_client)
        fstorage.bytes_to_blob(path01,b'',s3_client)
        fstorage.bytes_to_blob(path02,b'',s3_client)
        
        self.assertTrue(fstorage.is_blob_exist(path000,s3_client))
        self.assertTrue(fstorage.is_blob_exist(path001,s3_client))
        self.assertTrue(fstorage.is_blob_exist(path01,s3_client))
        self.assertTrue(fstorage.is_blob_exist(path02,s3_client))
        
        fstorage.rmtree(path00,s3_client)
        
        self.assertFalse(fstorage.is_blob_exist(path000,s3_client))
        self.assertFalse(fstorage.is_blob_exist(path001,s3_client))
        self.assertTrue(fstorage.is_blob_exist(path01,s3_client))
        self.assertTrue(fstorage.is_blob_exist(path02,s3_client))

    @unittest.skip("fat case")
    def test_rmtree_big(self):
        timestamp = int(time.time())

        s3_client = fstorage.create_client()

        path0 = f's3://futsu-test/test-HOSPFEUB-{timestamp}'
        for i in range(1234):
            print(f'UQYFVDQC create {i}')
            path00 = fstorage.join(path0,str(i))
            fstorage.bytes_to_blob(path00,b'',s3_client)
            self.assertTrue(fstorage.is_blob_exist(path00,s3_client))

        self.assertEqual(len(list(fstorage.find_blob_itr(path0,s3_client))),1234)

        print('TLWHHGHX rmtree')
        fstorage.rmtree(path0,s3_client)

        self.assertEqual(len(list(fstorage.find_blob_itr(path0,s3_client))),0)

        for i in range(1234):
            print(f'UQYFVDQC check {i}')
            path00 = fstorage.join(path0,str(i))
            self.assertFalse(fstorage.is_blob_exist(path00,s3_client))
