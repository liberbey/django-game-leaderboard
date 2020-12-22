# Django Game Leaderboard

## Description

Project aims to create an **efficient leaderboard** for games with millions of users. In order to make responses fast, **Redis** Sorted Sets and Hashes are used.  

## Technologies

**Redis** is used as an in-memory database to decrease response time. **Silk** (/silk) is used for request monitoring. Application is deployed to **Heroku** and using the **PostgreSql** database provided by Heroku. Also a free Redis server is used which is provided by Redis Labs. Due to the restrictions of these free services, responses may be slow.

For a deployment, please comment the "django_heroku.settings(locals())" line in settings.py, edit database configurations in settings.py and edit redis configurations in api/core/constants.py. 

Note: Memory usage of Redis can be calculated as N * 400 bytes where N is the number of users.

## Endpoints

You can also check /swagger for endpoints.

### GET /api/leaderboard

Lists all users in the leaderboard with their ranks and points.

Response:

```
[
    {
        "country": "dm",
        "display_name": "wenypuq",
        "rank": 1,
        "score": 1762
    },
    {
        "country": "ao",
        "display_name": "ybockrv",
        "rank": 2,
        "score": 1626
    },
    {
        "country": "ad",
        "display_name": "rwvddlv",
        "rank": 3,
        "score": 1602
    },
...
]
```

Note: Since this endpoint possibly returns millions of json objects, it is not recommended to use. 

### GET /api/leaderboard/stream

Lists all users in the leaderboard with their ranks and points as a stream. Data will be served as chunks.

Response:

```
[
    {
        "country": "dm",
        "display_name": "wenypuq",
        "rank": 1,
        "score": 1762
    },
    {
        "country": "ao",
        "display_name": "ybockrv",
        "rank": 2,
        "score": 1626
    },
    {
        "country": "ad",
        "display_name": "rwvddlv",
        "rank": 3,
        "score": 1602
    },
...
]
```


### GET /api/leaderboard/range

Lists all users in the leaderboard in given range with their ranks and points. This is the recommended endpoint for retrieving leaderboard data, possibly with using pagination in the frontend. Please note that leaderboards are 0-indexed.

Request:

/api/leaderboard/range/?start=0&offset=3


Response:

```
[
    {
        "country": "dm",
        "display_name": "wenypuq",
        "rank": 1,
        "points": 1762
    },
    {
        "country": "ao",
        "display_name": "ybockrv",
        "rank": 2,
        "points": 1626
    },
    {
        "country": "ad",
        "display_name": "rwvddlv",
        "rank": 3,
        "points": 1602
    }
]
```

### GET /api/leaderboard/<iso_code>

Lists all users in the leaderboard of given country with their ranks and points.

Request:

/api/leaderboard/tr

Response:

```
[
    {
        "country": "tr",
        "display_name": "srnmitg",
        "rank": 6,
        "points": 1545
    },
    {
        "country": "tr",
        "display_name": "uecmats",
        "rank": 10,
        "points": 1505
    },
    {
        "country": "tr",
        "display_name": "nyfvpyf",
        "rank": 15,
        "points": 1437
    },
...
]
```

Note: Since this endpoint possibly returns millions of json objects, it is not recommended to use. 

### GET /api/leaderboard/<iso_code>/stream

Lists all users in the leaderboard of given with their ranks and points as a stream. Data will be served as chunks.

Request:

/api/leaderboard/tr/stream

Response:

```
[
    {
        "country": "tr",
        "display_name": "srnmitg",
        "rank": 6,
        "points": 1545
    },
    {
        "country": "tr",
        "display_name": "uecmats",
        "rank": 10,
        "points": 1505
    },
    {
        "country": "tr",
        "display_name": "nyfvpyf",
        "rank": 15,
        "points": 1437
    },
...
]
```

### GET /api/leaderboard/<iso_code>/range

Lists all users in the leaderboard of given country in given range with their ranks and points. This is the recommended endpoint for retrieving leaderboard data, possibly with using pagination in the frontend. Please note that leaderboards are 0-indexed.

Request:

/api/leaderboard/tr/range/?start=0&offset=3


Response:

```
[
    {
        "country": "tr",
        "display_name": "srnmitg",
        "rank": 6,
        "points": 1545
    },
    {
        "country": "tr",
        "display_name": "uecmats",
        "rank": 10,
        "points": 1505
    },
    {
        "country": "tr",
        "display_name": "nyfvpyf",
        "rank": 15,
        "points": 1437
    }
]
```

### POST api/score/submit

This enpoint allows you to add points to existing users.

Request:

/api/score/submit

```
{
    "user_id": "66fd39d3-4314-11eb-8807-d8c0a63e9fd8",
    "score_worth": 2899.72,
    "timestamp": 1608659589,  **not necessary, will be now automatically
}
```

Response:

```
{
    "user_id": "66fd39d3-4314-11eb-8807-d8c0a63e9fd8",
    "score_worth": 99.72,
    "timestamp": "2020-12-22T20:53:09Z"
}
```

### GET /api/user/profile/<guid>

Returns user information with given id.

Request:

/api/user/profile/66fd39d3-4314-11eb-8807-d8c0a63e9fd8

Response:

```
{
    "country": "tr",
    "display_name": "uecmats",
    "user_id": "66fd39d3-4314-11eb-8807-d8c0a63e9fd8",
    "points": 13204,
    "rank": 1
}
```

### POST /user/create

Create a user.

Request:

```
{
    "user_id: "66fd39d3-4314-11eb-8807-d8c0a63e9f99",
    "display_name: "gjg",
    "country": "tr"
}
```

Response:

```
{
    "user_id": "66fd39d3-4314-11eb-8807-d8c0a63e9f99",
    "display_name": "gjg",
    "country": "tr",
    "rank": 85500,
    "points": 0
}

```
