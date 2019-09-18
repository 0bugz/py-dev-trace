import os
import sys
import json
import inspect
import logging
import threading

import core

class ZBLogger(logging.Logger):

    def error(self, msg, *args, **kwargs):
        super().error(msg, *args, **kwargs)
        print("ZBLogger error invoked ...: {}".format(msg))
        frame = inspect.currentframe()
        # The current frame is our frame - let us ignore it :)
        event = {
            "ip_address": core.ip_address,
            "thread_name":threading.currentThread().name,
            "stack":[]
        }
        caller = frame.f_back
        while None != caller:
            resp = self.get_frame_details(caller)
            # print(resp["frame_details"])
            event["stack"].append(json.dumps(resp["frame_details"]))
            # caller = None
            caller = resp["calling_frame"]
        core.worker_pool.queue_message(json.dumps(event))

    def is_json_serializable(self, val):
        try:
            json.dumps(val)
            return True
        except:
            return False

    def is_internal_key(self, key):
        if key != None:
            if key.startswith("__") and key.endswith("__"):
                return True
        return False

    def get_object_attributes(self, obj):
        ret_val = {}
        if obj != None:
            attributes = obj.__dict__
            for k, v in attributes.items():
                if not self.is_internal_key(k) and \
                    not inspect.ismodule(v):
                    ret_val[k] = v
        return ret_val

    def get_object_json(self, obj):
        ret_val = {}
        if obj != None:
            if not inspect.ismodule(obj) and hasattr(obj, "__dict__"):
                attributes = self.get_object_attributes(obj)
                for k, v in attributes.items():
                    if not self.is_internal_key(k):
                        if self.is_json_serializable(v):
                            ret_val[k] = v
                        else:
                            ret_val[k] = self.get_object_json(v)
        return ret_val

    def get_variable_dict(self, frame_vars):
        ret_val = {}
        for k, v in frame_vars:
            if not self.is_internal_key(k):
                if self.is_json_serializable(v):
                    ret_val[k] = v
                else:
                    ret_val[k] = self.get_object_json(v)
        return ret_val

    def get_frame_details(self, frame):
        frame_details = {
            "file_name": frame.f_code.co_filename,
            "function_name": frame.f_code.co_name,
            "globals": {},
            "locals": {}
        }
        ret_val = self.get_variable_dict(frame.f_globals.items())
        for k, v in ret_val.items():
            if v:
                frame_details["globals"][k] = v

        ret_val = self.get_variable_dict(frame.f_locals.items())
        for k, v in ret_val.items():
            if v:
                frame_details["locals"][k] = v

        calling_frame = None
        if frame.f_back:
            calling_frame = frame.f_back

        return {"frame_details": frame_details, "calling_frame": calling_frame}
