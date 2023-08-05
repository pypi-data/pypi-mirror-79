import requests

BASE_URL = 'https://crawler.pylab.co'


class Session(object):
    def __init__(self, key):
        try:
            res = requests.get(f'{BASE_URL}/api/sdk/keys/?key={key}')
            res.raise_for_status()
            data = res.json()
            if len(data) == 0:
                raise InterruptedError()
            if not data['isActive']:
                raise InterruptedError()
            self.key = key
            self.group_id = data['group']
            self.group_name = data['groupName']
        except:
            raise PermissionError(f'API 키({key})가 유효하지 않습니다.')

    def add_log(self, task_id: int, content: str) -> None:
        """로그를 기록"""
        if not task_id:
            return
        try:
            res = requests.post(f'{BASE_URL}/api/sdk/task-logs/?key={self.key}', data={
                'task': task_id,
                'content': content
            })
            res.raise_for_status()
        except:
            pass

    def is_running(self, task_id: int) -> bool:
        """태스크가 아직 실행중인지 확인"""
        if not task_id:
            return True

        retry_cnt = 0
        while retry_cnt < 3:
            try:
                res = requests.get(f'{BASE_URL}/api/sdk/tasks/{task_id}/?key={self.key}')
                res.raise_for_status()
                data = res.json()
                if data['status'] in ['progress', 'pending']:
                    break
                else:
                    return False
            except:
                pass
            retry_cnt += 1

        if retry_cnt >= 3:
            return False

        try:
            res = requests.get(f'{BASE_URL}/api/sdk/task-terminations/?key={self.key}&task={task_id}')
            res.raise_for_status()
        except:
            return True
        data = res.json()
        return len(data) == 0

    def create_task_type(self, module_name, function_name, kwargs, description) -> int:
        """태스크 타입을 생성"""
        res = requests.post(
            f'{BASE_URL}/api/sdk/tasks/?key={self.key}',
            data={
                'moduleName': module_name,
                'functionName': function_name,
                'kwargs': kwargs,
                'description': description
            }
        )
        res.raise_for_status()
        task_type = res.json()
        return task_type['id']

    def delete_task_type(self, task_type_id) -> int:
        """태스크 타입을 삭제"""
        res = requests.delete(
            f'{BASE_URL}/api/sdk/task-types/{task_type_id}/?key={self.key}'
        )
        res.raise_for_status()

    def create_task(self, task_type_id) -> int:
        """태스크를 생성"""
        res = requests.post(
            f'{BASE_URL}/api/sdk/tasks/?key={self.key}',
            data={
                'taskType': task_type_id
            }
        )
        res.raise_for_status()
        task = res.json()
        return task['id']

    def terminate_task(self, task_id) -> None:
        """태스크를 종료"""
        res = requests.post(
            f'{BASE_URL}/api/sdk/task-terminations/?key={self.key}',
            data={
                'task': task_id
            }
        )
        res.raise_for_status()

    def write_file(self, filename, blob) -> None:
        """파일을 생성"""
        res = requests.post(
            f'{BASE_URL}/api/sdk/storage/?key={self.key}',
            files={'file': blob},
            data={'filename': filename}
        )
        res.raise_for_status()

    def read_file(self, filename) -> None:
        """파일을 읽기"""
        res = requests.get(
            f'https://storage.googleapis.com/pylab-crawler-storage/{self.group_name}/{filename}'
        )
        res.raise_for_status()
        res.raw.decode_content = True
        return res.raw.read()

    def delete_file(self, filename) -> None:
        """파일을 삭제"""
        res = requests.delete(
            f'{BASE_URL}/api/sdk/storage/?key={self.key}&filename={filename}'
        )
        res.raise_for_status()
