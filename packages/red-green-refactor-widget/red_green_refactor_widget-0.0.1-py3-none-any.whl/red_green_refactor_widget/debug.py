import inspect

def not_implemented():
    prev_frame = inspect.currentframe().f_back
    prev_frame_info = inspect.getframeinfo(prev_frame)
    print("{}:{} Not implemented"
        .format(prev_frame_info.filename, prev_frame_info.lineno))
