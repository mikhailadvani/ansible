from ansible.module_utils.basic import *
from ansible.module_utils.pycompat24 import get_exception
import os

def get_all_files(path):
    objects = os.listdir(path)
    files = []
    for object in objects:
        if os.path.isfile(path + object ):
            files.append(object)
    return files

def list_diff(all_files,files_to_retain):
    return list(set(all_files) - set(files_to_retain))

def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(required=True, type='str'),
            file_list=dict(required=True, type='list')
        ),
        supports_check_mode=True
    )
    path = module.params['path'] if module.params['path'][-1] == '/' else module.params['path'] + '/'
    files_to_retain = module.params['file_list']
    all_files = get_all_files(path)
    files_to_delete = list_diff(all_files, files_to_retain)
    try:
        if len(files_to_delete) > 0:
            if not module.check_mode:
                for file in files_to_delete:
                    os.remove(path+file)
            module.exit_json(changed=True, msg="Files to delete:%s" % ",".join(files_to_delete))
        else:
            module.exit_json(changed=False, msg="Nothing to delete")
    except Exception:
        e = get_exception()
        module.fail_json(msg="%s" % str(e))


if __name__ == '__main__':
    main()
