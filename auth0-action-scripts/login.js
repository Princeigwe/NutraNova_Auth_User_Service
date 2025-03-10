function login(email, password, callback) {
  //this example uses the "pg" library
  //more info here: https://github.com/brianc/node-postgres

  const { Pool } = require('pg');
  const bcrypt = require('bcrypt');

  process.env.NODE_TLS_REJECT_UNAUTHORIZED=0;
  
  const pool = new Pool({
    connectionString: process.env.AIVEN_DATABASE_URI,
    ssl: {
      rejectUnauthorized: false
    }
  });

  pool.connect(function (err, client, done) {
    if (err) return callback(err);

    const query = 'SELECT id, email, password FROM public.users_customuser WHERE email = $1';
    client.query(query, [email], function (err, result) {
      // NOTE: always call `done()` here to close
      // the connection to the database
      done();

      if (err || result.rows.length === 0) return callback(err || new WrongUsernameOrPasswordError(email));

      const user = result.rows[0];

      bcrypt.compare(password, user.password, function (err, isValid) {
        if (err || !isValid) return callback(err || new WrongUsernameOrPasswordError(email));

        return callback(null, {
          user_id: user.id,
          // nickname: user.nickname,
          email: user.email
        });
      });
    });
  });
}
