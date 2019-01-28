def dict_fetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


# def get_permission_dict(permission_result):
#     permission_dict = dict()
#     for each in permission_result:
#         aid = each.get('AID')
#         pid = each.get('PID')
#         fid = each.get('FID')
#         gname = each.get('GName')
#         pname = each.get('PName')
#         fname = each.get('FName')
#         if aid not in permission_dict:
#             permission_dict[aid] = {
#                 'GName': gname,
#                 pid: {
#                     'PName': pname,
#                     fid: {
#                         'FName': fname
#                     }
#                 }
#             }
#         else:
#             if pid not in permission_dict[aid]:
#                 permission_dict[aid][pid] = {
#                     'PName': pname,
#                     fid: {
#                         'FName': fname
#                     }
#                 }
#             else:
#                 if fid not in permission_dict[aid][pid]:
#                     permission_dict[aid][pid][fid] = {
#                         'FName': fname
#                     }
#     return permission_dict
