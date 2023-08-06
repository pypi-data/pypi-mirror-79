# -*- coding: utf-8 -*- --------------------------------------------------===#
#
#  Copyright 2018-2020 Trovares Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#===----------------------------------------------------------------------===#

from datetime import datetime
import logging
import json
import six

from . import ErrorMessages_pb2 as err_proto
from . import JobService_pb2 as job_proto
from . import SchemaMessages_pb2 as sch_proto
from .common import (XgtError, XgtInternalError, _to_unicode, _to_str,
                     _code_error_map)

log = logging.getLogger(__name__)

class Job(object):
  """
  Represents a user-scheduled Job.

  An instance of this object is created by job-scheduling functions like
  `xgt.Connection.run_job` and `xgt.Connection.schedule_job`.

  A `Job` is used as a proxy for a job in the server and allows the user
  to monitor its execution, possibly cancel it, and learn about its status
  during and after execution.

  The conn parameter represents a previously established connection to the xGT
  server.

  The job_response parameter is a single element of the array returned by the
  output of a job creation gRPC call.  Each individual element in the array will
  be constructed as a separate `Job` object.

  """
  def __init__(self, conn, job_response):
    """
    Constructor for Job. Called when Job is created.
    """
    self._conn = conn
    self._id = job_response.job_id
    self._user = job_response.user
    self._data = self._parse_job_data(job_response)

  def _parse_job_data(self, job_response):
    job_data = {
      'jobid': job_response.job_id,
      'user': job_response.user,
      'status': sch_proto.JobStatusEnum.Name(job_response.status).lower(),
      'start_time': job_response.start_time.ToDatetime().isoformat(),
      'end_time': job_response.end_time.ToDatetime().isoformat(),
      'error_type': None,
      'visited_edges': job_response.visited_edges,
      'timing': job_response.timing,
      'description': job_response.description,
      'total_rows' : job_response.total_rows,
    }
    # Optional fields.
    if (job_response.HasField('schema')):
      job_data['schema'] = [[prop.name,
                             sch_proto.UvalTypeEnum.Name(prop.data_type).lower()]
                            for prop in job_response.schema.property]
    if job_response.row and len(job_response.row) > 0:
      job_data['rows'] = [data for data in job_response.row]
    if job_response.error and len(job_response.error) > 0:
        error_code_name = err_proto.ErrorCodeEnum.Name(job_response.error[0].code)
        job_data['error_type'] = _code_error_map[error_code_name]
        job_data['error'] = ', '.join([e.message for e in job_response.error])
        job_data['trace'] = ', '.join([e.detail for e in job_response.error])
    return job_data

  def _get_job_data(self):
    request = job_proto.GetJobsRequest()
    request.job_id.extend([self._id])
    responses = self._conn._call(request, self._conn._job_svc.GetJobs)
    job_data = None
    resp_cnt = 0
    for response in responses: # Expect only one response.
      job_data = self._parse_job_data(response.job_status) # Retrieve the job status.
      resp_cnt += 1

    if (resp_cnt > 1):
      raise XgtInternalError("Expected a single job in response")

    # Cache the response from the server.
    self._data = job_data

    if log.getEffectiveLevel() >= logging.DEBUG:
      job_id = job_data['jobid']
      job_status = job_data['status']
      user = job_data['user']
      if 'error' in job_data:
        error = job_data['error']
      else:
        error = ''
      if 'trace' in job_data:
        trace = job_data['trace']
      else:
        trace = ''
      msg = u'Job: {0} User: {1} Status: {2}'.format(_to_unicode(job_id),
                                                     user,
                                                     job_status)
      if error != '':
        msg = msg + "\nError: \n" + error
      if trace != '':
        msg = msg + "\nTrace: \n" + trace
      log.debug(msg)

    return job_data

  def _is_status_final(self):
    if 'status' in self._data:
      curr_status = self._data['status']

      if ((curr_status == 'completed') or (curr_status == 'canceled') or
          (curr_status == 'failed') or (curr_status == 'rollback')):
        return True

    return False

  def _get_data_helper(self, offset, length):
    if 'rows' in self._data:
      if isinstance(offset, six.string_types):
        offset = int(offset)
      if isinstance(length, six.string_types):
        length = int(length)
      if isinstance(offset, int):
        if offset < 0:
          raise ValueError('offset is negative')
      if isinstance(length, int):
        if length < 0:
          raise ValueError('length is negative')
      total_length = len(self._data['rows'])
      if length is None:
        length = total_length
      elif not isinstance(length, int):
        raise ValueError('length must be a non-negative integer')

      # Uses JSON conversion.
      res = ''
      pos = 0
      rows = self._data['rows']
      startpos = min(offset, total_length)
      endpos = min(offset + length + 1, total_length)

      while (startpos < endpos):
        row = rows[startpos]
        if (startpos < (endpos - 1)):
          res += (row + ',')
        else:
          res += (row)
        startpos += 1
      try:
        jsn = json.loads('['+res+']')
      except ValueError as ex:
        raise XgtInternalError('Invalid JSON format: '+_to_unicode(ex))
      return jsn
    else:
      return None

  @property
  def id(self):
    """
    int: Identifier of the job.

    A 64-bit integer value that uniquely identifies a job. It is
    automatically incremented for each scheduled job over the lifetime of
    the xGT server process.

    """
    return self._id

  @property
  def user(self):
    """
    str: User that ran the job.

    A string that identifies the user who ran the job.
    """
    return self._user

  @property
  def status(self):
    """
    str: Status of the job.

  ==================  ===============================================
        Job status
  -------------------------------------------------------------------
           Status                       Description
  ==================  ===============================================
           scheduled  The state after the job has been created, but
                      before it has started running.
             running  The job is being executed.
           completed  The job finished successfully.
            canceled  The job was canceled.
              failed  The job failed. When the job fails the `error`
                      and `trace` properties are populated.
            rollback  The job had a transactional conflict with
                      another job and was rolled back.
  unknown_job_status  The job was not found in job history.
  ==================  ===============================================

    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'status' in self._data:
      return _to_unicode(self._data['status'])
    else:
      return ''

  @property
  def start_time(self):
    """
    str: Date and time when the job was scheduled.

    This is a formatted string that has a resolution of seconds.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'start_time' in self._data:
      if "." in self._data['start_time']:
        return datetime.strptime(self._data['start_time'], '%Y-%m-%dT%H:%M:%S.%f')
      return datetime.strptime(self._data['start_time'], '%Y-%m-%dT%H:%M:%S')
    else:
      return ''

  @property
  def end_time(self):
    """
    str: Date and time when the job finished running.

    This is a formatted string that has a resolution of seconds.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'end_time' in self._data:
      if "." in self._data['start_time']:
        return datetime.strptime(self._data['end_time'], '%Y-%m-%dT%H:%M:%S.%f')
      return datetime.strptime(self._data['end_time'], '%Y-%m-%dT%H:%M:%S')
    else:
      return ''

  @property
  def visited_edges(self):
    """
    dict: A dictionary mapping Cypher bound variable names to an integer giving
    the number of edges visited during the job for the Edge Frame referenced by
    the bound variable.

    An edge is "visited" when the query considers the edge as a match to one of
    the query path edges.  Multiple Cypher variables can refer to the same edge
    frame.

    Consider the query path
    ``()-[a:graph_edges1]->()-[b:graph_edges2]->()-[c:graph_edges1]->()`` with
    a visited_edges result of ``a -> 5, b -> 7, c -> 4``.  In performing the
    query 5 edges of type `a` were visited, and so on.  Notice that the total
    number of edges visited for the frame graph_edges1 is 9 while the number of
    edges visited for the frame graph_edges2 is 7.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    return self._data['visited_edges']

  @property
  def total_visited_edges(self):
    """
    int: The total number of edges traversed during the job. This is the sum
    of the counts for all edge labels returned in visited_edges.

    For the example given in the visited_edges documentation, the value of
    total_visited_edges would be 16.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    return sum(self._data['visited_edges'].values())

  @property
  def timing(self):
    """
    For internal use.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    return self._data['timing']

  @property
  def description(self):
    """
    str: A description supplied when the job was started.  Usually a query.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    return self._data['description']

  @property
  def error_type(self):
    """
    object: Class that belongs to the XgtError hierarchy that corresponds to
            the original exception type thrown that caused the Job to fail.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'error_type' in self._data:
      return self._data['error_type']
    else:
      return XgtError

  @property
  def error(self):
    """
    str: User-friendly error message describing the reason a job failed.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'error' in self._data:
      return _to_unicode(self._data['error'])
    else:
      return ''

  @property
  def trace(self):
    """
    str: Very detailed error message for a failed job.

    This error message contains the friendly error message and a stack
    strace for the code that participated in the error.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'trace' in self._data:
      return _to_unicode(self._data['trace'])
    else:
      return ''

  @property
  def schema(self):
    """
    list of lists: Gets the property names and types of the stored immediate
    results.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'schema' in self._data:
      return self._data['schema']
    else:
      return None

  @property
  def total_rows(self):
    """
    int: Gets the number of rows of the query results.  Note that this is >=
    than the number of rows of data extracted to the job.  To get the full
    results the query can be executed again using an INTO clause to a
    named results Table.
    """
    if (not self._is_status_final()):
      self._get_job_data()

    if 'total_rows' in self._data:
      return self._data['total_rows']
    else:
      return None

  def get_data(self, offset=0, length=None):
    """
    Returns immediate results data starting at a given offset and spanning a given
    length.

    Parameters
    ----------
    offset : int
      Position (index) of the first row to be retrieved.
      Optional. Default=0.
    length : int
      Maximum number of rows to be retrieved starting from the row
      indicated by offset. A value of 'None' means 'all rows' on and
      after the offset.
      Optional. Default=None.

    Returns
    -------
    list of lists

    """
    if (not self._is_status_final()):
      self._get_job_data()

    jsn = self._get_data_helper(offset, length)
    if jsn is not None:
      return jsn[1:]
    else:
      return None

  def get_data_pandas(self, offset=0, length=None):
    """
    Returns a Pandas DataFrame containing immediate results data starting at a
    given offset and spanning a given length.

    Parameters
    ----------
    offset : int
      Position (index) of the first row to be retrieved.
      Optional. Default=0.
    length : int
      Maximum number of rows to be retrieved starting from the row
      indicated by offset. A value of 'None' means 'all rows' on and
      after the offset.
      Optional. Default=None.

    Returns
    -------
    Pandas DataFrame

    """
    import pandas
    # Uses JSON conversion.
    if (not self._is_status_final()):
      self._get_job_data()

    jsn = self._get_data_helper(offset, length);
    if jsn is not None:
      return pandas.DataFrame(columns=jsn[0:1][0], data=jsn[1:])
    else:
      return None

  def __str__(self):
    txt = (u'id:{0}, user:{1}, status:{2}').format(self.id, self.user, self.status)
    if len(self.error) > 0:
      txt = txt + (u', nerror:{0}').format(self.error)
    return _to_str(txt)

