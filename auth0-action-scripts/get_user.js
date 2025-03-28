function loginByEmail(email, callback) {
  //this example uses the "pg" library
  //more info here: https://github.com/brianc/node-postgres

  const { Client } = require('pg');

  const conString = process.env.AIVEN_DATABASE_URI;

  const client = new Client({
    connectionString: conString
  });

  client.connect(conString, function (err, client, done) {
    if (err) return callback(err);

    const query = 'SELECT id, email FROM public.users_customuser WHERE email = $1';
    client.query(query, [email], function (err, result) {
      // NOTE: always call `done()` here to close
      // the connection to the database
      done();

      if (err || result.rows.length === 0) return callback(err);

      const user = result.rows[0];

      return callback(null, {
        user_id: user.id,
        // nickname: user.nickname,
        email: user.email
      });
    });
  });
}
