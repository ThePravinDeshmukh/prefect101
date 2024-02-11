https://github.com/rpeden/prefect-docker-compose/tree/main

        docker pull prefecthq/prefect:2.14-python3.8-kubernetes


To start server: 

        docker-compose --profile server up -d

question:
1. Why do we need an agent?


Once server is up and running
Test
        http://localhost:4200/deployments
or
        http://host.docker.internal:4200/deployments

Both works and are same!

Connect your local prefect to docker

        prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"

question:
1. Why do we have to do that?
  Probably because docker is still treated as remote server so prefect cli need to knows config to connect to docker api

To deploy flows in container:

        PS D:\Code\Git\prefect101> kubectl apply -f deployments/flow-manifest.yaml

This will spin up deployment and pod

    PS D:\Code\Git\prefect101> kubectl get deployments               
    NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
    prefect-docker-guide   1/1     1            1           4m17s
    PS D:\Code\Git\prefect101> kubectl get pods
    NAME                                    READY   STATUS    RESTARTS   AGE
    prefect-docker-guide-6cf978957c-65968   1/1     Running   0          4m20s
    PS D:\Code\Git\prefect101> kubectl logs prefect-docker-guide-6cf978957c-65968
    Your flow 'get-repo-info' is being served and polling for scheduled runs!

        To trigger a run for this flow, use the following command:

        $ prefect deployment run 'get-repo-info/prefect-docker-guide'

You can also run your flow via the Prefect UI: http://host.docker.internal:4200/deployments/deployment/3dffcc18-cc3d-42c6-b1e6-3855869e705d

        09:07:46.878 | INFO    | prefect.flow_runs.runner - Runner 'prefect-docker-guide' submitting flow run '96aac0ca-68c7-445a-a643-135daa6537e5'
        09:07:46.969 | INFO    | prefect.flow_runs.runner - Opening process...
        09:07:46.980 | INFO    | prefect.flow_runs.runner - Completed submission of flow run '96aac0ca-68c7-445a-a643-135daa6537e5'
        /usr/local/lib/python3.10/runpy.py:126: RuntimeWarning: 'prefect.engine' found in sys.modules after import of package 'prefect', but prior to execution of 'prefect.engine'; this may result in unpredictable behaviour
        warn(RuntimeWarning(msg))
        09:07:48.490 | INFO    | Flow run 'papaya-vicugna' - Downloading flow code from storage at '.'
        09:07:49.209 | INFO    | Flow run 'papaya-vicugna' - PrefectHQ/prefect repository statistics 🤓:
        09:07:49.210 | INFO    | Flow run 'papaya-vicugna' - Stars 🌠 : 14015
        09:07:49.212 | INFO    | Flow run 'papaya-vicugna' - Forks 🍴 : 1432
        09:07:50.928 | INFO    | Flow run 'papaya-vicugna' - Finished in state Completed()
        09:07:51.324 | INFO    | prefect.flow_runs.runner - Process for flow run 'papaya-vicugna' exited cleanly.
        09:08:20.408 | INFO    | prefect.flow_runs.runner - Runner 'prefect-docker-guide' submitting flow run '57260bc7-2300-4f12-8e2f-e7f101e4e660'
        09:08:20.435 | INFO    | prefect.flow_runs.runner - Opening process...
        09:08:20.438 | INFO    | prefect.flow_runs.runner - Completed submission of flow run '57260bc7-2300-4f12-8e2f-e7f101e4e660'
        /usr/local/lib/python3.10/runpy.py:126: RuntimeWarning: 'prefect.engine' found in sys.modules after import of package 'prefect', but prior to execution of 'prefect.engine'; this may result in unpredictable behaviour
        warn(RuntimeWarning(msg))
        09:08:21.776 | INFO    | Flow run 'delightful-kakapo' - Downloading flow code from storage at '.'
        09:08:22.256 | INFO    | Flow run 'delightful-kakapo' - PrefectHQ/prefect repository statistics 🤓:
        09:08:22.258 | INFO    | Flow run 'delightful-kakapo' - Stars 🌠 : 14015
        09:08:22.259 | INFO    | Flow run 'delightful-kakapo' - Forks 🍴 : 1432
        09:08:23.289 | INFO    | Flow run 'delightful-kakapo' - Finished in state Completed()
        09:08:23.694 | INFO    | prefect.flow_runs.runner - Process for flow run 'delightful-kakapo' exited cleanly.



To start deployment via Cli:

        
        PS D:\Code\Git\prefect101> prefect deployment run get-repo-info/prefect-docker-guide
        Creating flow run for deployment 'get-repo-info/prefect-docker-guide'...
        Created flow run 'delightful-kakapo'.
        └── UUID: 57260bc7-2300-4f12-8e2f-e7f101e4e660
        └── Parameters: {}
        └── Scheduled start time: 2024-02-11 14:38:17 IST (now)
        └── URL: http://127.0.0.1:4200/flow-runs/flow-run/57260bc7-2300-4f12-8e2f-e7f101e4e660

To start deployment via UI:

Deployments > Select prefect-docker-guide > Quick run

Navigate to flow runs to check generated run, its status and logs.


Stop all:

        kubectl delete -f deployments/flow-manifest.yaml
        docker-compose --profile server down 

Start everything back:

        docker-compose --profile server up -d

It remembers the deployment and previous runs because of Postgres database.

Next Actions:

Prefect server is started in docker and flows are then deployed as container in k8s
Prefect Server also needs to start in k8s.


prefect kubernetes manifest server > server-manifest.yaml
prefect kubernetes manifest agent > agent-manifest.yaml  

Start Server
    kubectl apply -f .\deployments\server-manifest.yaml
    kubectl apply -f .\deployments\agent-manifest.yaml

Forward port

    kubectl port-forward deployments/prefect-server 4200:4200 -n default

Set local prefect config to point to k8s

    prefect config set PREFECT_API_URL=http://localhost:4200/api

For debugging in Pod

        kubectl exec --stdin --tty pod-name -- /bin/bash
        apt update
        apt install curl
        curl -I -L http://prefect-server:4200

        PS D:\Code\Git\prefect101> prefect deployment run get-repo-info/prefect-docker-guide  
        Creating flow run for deployment 'get-repo-info/prefect-docker-guide'...
        Created flow run 'classy-chameleon'.
        └── UUID: c5afde77-aeb0-4af8-b167-fe4ffa811e2e
        └── Parameters: {}
        └── Scheduled start time: 2024-02-11 16:02:21 IST (now)
        └── URL: http://localhost:4200/flow-runs/flow-run/c5afde77-aeb0-4af8-b167-fe4ffa811e2e

        
Worked! I am able to 
 - Run prefect server and agent in k8s
 - build and deploy prefect flow as container in k8s
 - schedule and run deployed flow using cli and ui

 Ref
  - docker based setup https://github.com/rpeden/prefect-docker-compose/blob/main/docker-compose.yml
  - k8s based https://discourse.prefect.io/t/deploying-prefect-agents-on-kubernetes/1298
  - little helpful https://www.restack.io/docs/prefect-knowledge-prefect-deployment-kubernetes
