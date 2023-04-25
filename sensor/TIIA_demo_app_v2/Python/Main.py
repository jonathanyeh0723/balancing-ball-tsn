from fastapi import Depends, FastAPI, Header, HTTPException
import json
from starlette.requests import Request
from starlette.responses import Response
from Intel_Kalycito_Opcus_Log_Processor import Intel_Kalycito_Opcus_Log_Processor 
from Intel_Kalycito_Opcus_Runner import Intel_Kalycito_Opcus_Runner 
import uvicorn


app = FastAPI()

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print(e)
        return Response("Internal server error", status_code=500)


uvicorn_config = {
    'host': '0.0.0.0',
    'port': 5000,
    'log_level': 'debug'
}

app = FastAPI()
max_entry_pub_queue_len = 30
max_entry_latency_result_queue_len = max_entry_pub_queue_len

@app.get("/latency")
async def root(response: Response):
    #add http header for cross site access
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "x-requested-with"
    num_values =60
    opcua_log_handler=Intel_Kalycito_Opcus_Log_Processor(max_entry_pub_queue_len  , max_entry_latency_result_queue_len)
    latency_avg = opcua_log_handler.get_avg_latency_values(num_values)
    latency_max = opcua_log_handler.get_max_latency_values(num_values)
    latency_min = opcua_log_handler.get_min_latency_values(num_values)
    return {"latency_list" : json.dumps(opcua_log_handler.pop_latency_values_list(num_values)), "avg_latency_val": latency_avg , "max_latency_val": latency_max, "min_latency_val": latency_min}

if __name__ == "__main__":
    opcua_runner=Intel_Kalycito_Opcus_Runner(max_entry_pub_queue_len , max_entry_latency_result_queue_len)
    opcua_runner.run()
    #opcua_runner.run_test()
    uvicorn.run(app, **uvicorn_config)
