"""
Tests for app.py
"""
import json

from views.history import history
from shared.tests.base import TestsBaseClass
from shared.utils import utils


class HistoryTests(TestsBaseClass):
    """
    Tests for app.py
    """

    def test_01_get_job_info(self):
        """
        Should return job info object.
        """

        job_id = "some-job-id"
        job_info = history.get_job_info(self.redis_conn, job_id)
        self.assertIsInstance(job_info, dict)

    def test_02_get_job_info_no_status_but_relics_exist(self):
        """
        Should return job info object and create job status entry.
        """

        relics = ["1", "2", "3"]
        sample = "some text sample"
        data = {"relics": relics, "sample": sample}
        job_id = "some-job-id"
        self.redis_conn.set(f"relics:{job_id}", json.dumps(data))
        job_info = history.get_job_info(self.redis_conn, job_id)
        job_status = self.redis_conn.hget("jobs:status", job_id)
        job_status = json.loads(job_status)
        self.assertTrue(job_status["success"])
        self.assertIsInstance(job_info, dict)

    def test_03_create_job_info_object_status_and_relics_exist(self):
        """
        Should return job object of correct structure.
        """

        relics = ["1", "2", "3"]
        sample = "some text sample"
        data = {"relics": relics, "sample": sample}
        job_id = "some-job-id"
        job_status = utils.mark_job_success(job_id, True, redis_conn=self.redis_conn)
        self.redis_conn.set(f"relics:{job_id}", json.dumps(data))
        job_object = history.create_job_info_object(job_status, relics, sample, job_id)
        self.assertIsInstance(job_object, dict)
        self.assertListEqual(job_object["relics"], relics)
        self.assertEqual(job_object["jobId"], job_id)
        self.assertEqual(job_object["timestamp"], job_status["timestamp"])
        self.assertTrue(job_object["success"])
        self.assertTrue(job_object["sample"], sample)
        self.assertFalse(job_object["inProgress"])

    def test_04_create_job_info_object_no_status_but_relics_exist(self):
        """
        Should return job object of correct structure.
        """

        relics = ["1", "2", "3"]
        sample = "some text sample"
        data = {"relics": relics, "sample": sample}
        job_id = "some-job-id"
        self.redis_conn.set(f"relics:{job_id}", json.dumps(data))
        job_object = history.create_job_info_object(None, relics, sample, job_id)
        self.assertIsInstance(job_object, dict)
        self.assertListEqual(job_object["relics"], relics)
        self.assertEqual(job_object["jobId"], job_id)
        self.assertEqual(job_object["sample"], sample)
        self.assertTrue("timestamp" not in job_object)
        self.assertFalse(job_object["success"])
        self.assertFalse(job_object["inProgress"])

    def test_05_create_job_info_object_status_exists_but_no_relics(self):
        """
        Should return job object of correct structure.
        """

        relics = []
        sample = "some text sample"
        job_id = "some-job-id"
        job_status = utils.mark_job_success(job_id, True, redis_conn=self.redis_conn)
        job_object = history.create_job_info_object(job_status, relics, sample, job_id)
        self.assertIsInstance(job_object, dict)
        self.assertListEqual(job_object["relics"], relics)
        self.assertEqual(job_object["jobId"], job_id)
        self.assertEqual(job_object["timestamp"], job_status["timestamp"])
        self.assertEqual(job_object["sample"], sample)
        self.assertEqual(job_object["success"], True)
        self.assertFalse(job_object["inProgress"])
        self.assertTrue(job_object["expired"])

    def test_06_create_job_info_object_status_exists_but_false_and_no_relics(self):
        """
        Should return job object of correct structure.
        """

        relics = []
        sample = "some text sample"
        job_id = "some-job-id"
        job_status = utils.mark_job_success(job_id, False, redis_conn=self.redis_conn)
        job_object = history.create_job_info_object(job_status, relics, sample, job_id)
        self.assertIsInstance(job_object, dict)
        self.assertListEqual(job_object["relics"], relics)
        self.assertEqual(job_object["jobId"], job_id)
        self.assertEqual(job_object["timestamp"], job_status["timestamp"])
        self.assertEqual(job_object["sample"], sample)
        self.assertEqual(job_object["success"], False)
        self.assertTrue(job_object["inProgress"])
        self.assertFalse(job_object["expired"])

    def test_07_create_job_info_object_status_and_relics_not_exist(self):
        """
        Should return job object of correct structure.
        """

        relics = []
        sample = "some text sample"
        job_id = "some-job-id"
        job_object = history.create_job_info_object(None, relics, sample, job_id)
        self.assertIsInstance(job_object, dict)
        self.assertListEqual(job_object["relics"], relics)
        self.assertEqual(job_object["jobId"], job_id)
        self.assertTrue("timestamp" not in job_object)
        self.assertListEqual(job_object["relics"], relics)
        self.assertEqual(job_object["success"], False)
        self.assertFalse(job_object["inProgress"])
        self.assertFalse(job_object["expired"])

    def test_08_get_jobs_info(self):
        """
        Return a list of jobs info objects.
        """

        payload = {"data": ["some-job-01", "some-job-02"]}
        response = self.app.post("/v1/api/history", json=payload, follow_redirects=True)
        data = json.loads(response.data.decode("utf8"))
        self.assertTrue(data["success"])
        self.assertIsInstance(data["data"], list)

    def test_09_get_jobs_info_no_job_ids(self):
        """
        Should return an error when no job ids were provided.
        """

        payloads = [{"data": None}, {"data": "wrong data type"}]
        for payload in payloads:
            response = self.app.post(
                "/v1/api/history", json=payload, follow_redirects=True
            )
            data = json.loads(response.data.decode("utf8"))
            self.assertFalse(data["success"])
            self.assertEqual(data["message"], "No job ids provided")
