const express = require('express');
const bodyParser = require('body-parser');
const { Op, literal } = require('sequelize');
const sequelize = require('./config');
const User = require('./models/user');
const path = require('path');
const fs = require('fs');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));


(async () => {
  await sequelize.sync({ force: true });
  console.log('DB 생성');
})();


(async () => {
  try {
    await sequelize.authenticate();
    console.log('✅ DB 연결 성공');
  } catch (error) {
    console.error('❌ DB 연결 실패:', error);
  }
})();


app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

app.get('/search', (req,res) => {
    res.sendFile(path.join(__dirname, 'views', 'search.html'))
})


app.post('/search', (req, res) => {

    const user_id = req.body.user_id
    const user_password = req.body.user_password
    User.findOne({
        where: or(
            literal('TRIM("user_id") = TRIM(:user_id)'),
            { user_password: user_password },
        ),
    replacements: { user_id: user_id },
    }).then(users => {
        res.json(users);
        console.log(users);
    }).catch(error => {
        console.error(error);
    });
})

app.get('/register', (req,res) => {
    res.sendFile(path.join(__dirname, 'views', 'register.html'))
})

app.post('/register', async(req, res) => {
    const { user_id, user_password } = req.body;

    try {
        await User.create({ user_id, user_password });
        res.send(`<p> 사용자 등록 완료 : ${user_id} ${user_password}</p> <p><a href="/">돌아가기</a></p>`);
    } catch(err) {
        res.status(500).send('오류'+err.message);
    }
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'views','login.html'))
});

// 로그인 처리 
app.post('/login', async (req, res) => {
  const { user_id, user_password } = req.body;

  try {
    const users = await User.findAll({
      where: {
        [Op.and]:[
        literal('soundex("user_password") = soundex(:user_password)'),
        { user_id: user_id},
      ]
    },
      replacements: {user_id, user_password},
    })

    if (users.length > 0) {
      res.send(`<p> 로그인 성공 ${users[0].user_id}</p>`);
    } else {
      res.send('<p> 로그인 실패</p>');
    }
  } catch (err) {
    res.status(500).send('오류: ' + err.message);
  }
});

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});

