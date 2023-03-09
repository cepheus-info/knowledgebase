# Microservices guidelines

## Introduction

This document is a collection of guidelines for building microservices. It is not a set of rules, but rather a set of recommendations that should be considered when building microservices. The guidelines are based on the experience of the authors and the community.

## Table of Contents

- [Introduction](#introduction)

- [Table of Contents](#table-of-contents)

- [General](#general)

- [Naming](#naming)

- [Documentation](#documentation)

- [Logging](#logging)

- [Monitoring](#monitoring)

- [Testing](#testing)

- [Security](#security)

- [Deployment](#deployment)

- [Communication](#communication)

- [Data](#data)

- [Caching](#caching)

- [Error Handling](#error-handling)

- [Performance](#performance)

- [Scalability](#scalability)

- [Observability](#observability)

- [References](#references)

## General

- The first law of Distributed Objects Design is: Don't distribute. If you don't need to distribute your application, don't do it. If you need to distribute your application, don't distribute your objects.

- From a Data Decoupling point of view, the following article is a good starting point: [https://martinfowler.com/articles/data-oriented-architecture.html](https://martinfowler.com/articles/data-oriented-architecture.html)

  Repetition is greater than reuse. Don't try to reuse code, but rather try to reuse the knowledge and the experience.