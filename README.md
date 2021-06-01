# Interview Calendar API

### How to run API

```
git clone git@gitlab.com:ki-group-pt/xgeekshq/assignments/be-assignment-dylodylo.git
cd be-assignment-dylodylo
sudo docker build --tag calendar_api:latest .
sudo docker run --name calendar_api -d -p 8000:8000 calendar_api:latest
```

### Already created users

- superuser (username: admin, password: admin, id: 1)
- recruiters (usernames: recruiter1, recruiter2, password: recruiter, id: 2, 3)
- candidates (usernames: candidate1, candidate2, password: recruiter, id: 4, 5)


### How to use API

**Add new slots**

Open browser on adress 127.0.0.1:8000. Authorize yourself as user you want to add slots for and use PUT bookmark. In request body replace `{}` after in `slots` key to `{'slots': [dates]}. In the end request body could look like this:
`"slots": {"slots":["20/06/2021 12:00-13:00", "20/06/2021 15:00-16:00"]}` 

**Get periods which are same for candidate and recruiters**

Open browser on adress 127.0.0.1:8000 and use GET bookmark. Put candidate id in `id` field and recruiters ids in `r_ids` field.
In response body you'll get list of all dates when recruiters and candidate are available.

### Things to improve

- Better tests
- Add database to container
- Distinction between recruiter and candidate