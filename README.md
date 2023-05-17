# Databox Web Application Service

## Purpose

    This web application allows user to create the relations database and perform aggregation operation on it through web interface.

## Features

    - Ceate, Delete, Update and Read Relation Database
    - a monitor to maintain the size of the database to the optimal size and perform necessary rebuilts.
    - Scalable in term of divide and conquer technique to perform aggregation in reasonable time
        + leverage the multi-process to do all aggregation
        + provide API to access the data fetched/aggregated
    - Live testable on machine in containerised format
    - testable code which assesses the func upon all the commits made to the branch `testing`
    - CI/CD implementation
    - DevOps implemented

## Flow of the Code

    Feature branch ---> Testing branch ---> Master branch

## Running Tests

    At the project directory level directory run the command,

`py -m unittest utility\test_core.py`
