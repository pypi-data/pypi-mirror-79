from kmon.kmon_api import KmonAPI, KmonException
import kmon.datetime
import kmon.numpy as np

try:
    timestamp = datetime.datetime.now().timestamp()        
    kmon = Kmon('http://localhost')
    kmon.set_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNqakB0d2lubGFiLmNvLmtyIiwidGltZSI6IjIwMjAtMDgtMjVUMDQ6NDE6NDEuMzE3WiIsImlhdCI6MTU5ODMzMDUwMSwiZXhwIjoxNjAwOTIyNTAxfQ.gxJiQdhwQlekMDvbzp29d7Gl5FRcJC7MBJ9B6EccFv4')    

    rhos = np.array([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9])
    ora_args = {'rhos': rhos,
                'seed': 1234,
                'max_N': 100}

    job_key = kmon.job_init('MLP_Simple',ora_args)

    for _ in range(ora_args['max_N']):
        rho = kmon.job_next(job_key)
		print(rho)
        obs = 0.1
        result = kmon.job_feedback(job_key,rho,obs)
        print(result)
    
    print('complete')
    t = datetime.datetime.now().timestamp() - timestamp
    print('operstaion time : ' + str(t))

except KmonException as e:
    print(e)
except Exception as e:
    print(e)
