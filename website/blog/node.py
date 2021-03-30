# User模型和权限之间可以通过以下几种方式来进行
# user.userpermissions.set(permission_list): 直接给定一个权限的列表
# user.userpermissions.add(permission,permission,...): 一个个添加权限
# user.userpermissions.remove(permission,permission,...): 一个个删除权限
# user.userpermissions.clear(): 清除权限
# user.has_perm('<app_name>.<codename>'): 判断是否拥有某个权限
# user.get_all_permission(): 获得所有权限


