# Prometheus, Grafana, and Alertmanager

## Issues

| No. | Name                                                                   | Assignee          | Labels |
| --- | ---------------------------------------------------------------------- | ----------------- | ------ |
| 1   | Cortex Rules Alert not sending to Webhook (Cortex 通知无法发出)        | Juntao            | bug    |
| 2   | Prometheus Stack not deployed to the internal cluster (内网未部署监控) | Zhao Kai / Li Jun | task   |

## Objectives

- Cortex Rules Alert should be able to send to Webhook

  Cortex Alerts / Grafana Alerts 是两种告警生成方式，Cortex Alerts 是 Prometheus 的告警，Grafana Alerts 是 Grafana 的告警。但是目前配置的 Grafana Alert Manager 是不支持 Cortex Alerts 的，所以需要配置单独的 Alert Manager 来支持 Cortex Alerts。

- Deploy Prometheus Stack to the internal cluster

  目前内网环境未部署监控，需要部署 Prometheus Stack 到内网环境。同时，需要 Alert Service Webhook 服务分别部署在内网和外网环境，以便内网和外网环境的告警都能够发送到 Alert Service Webhook 服务。

  网络拓扑如下：

  - Alert Manager (内网区) -> Alert Service Webhook (内网区) -> Nginx 代理 (互联网区) -> Alert Client (公网服务器)
  - Alert Manager (互联网区) -> Alert Service Webhook (互联网区) -> Nginx 代理 (互联网区) -> Alert Client (公网服务器)
