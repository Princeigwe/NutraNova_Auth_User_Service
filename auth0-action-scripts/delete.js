function remove(user, callback) {
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

    const query = 'DELETE FROM public.users_customuser WHERE email = $1';
    client.query(query, [user.email], function (err) {
      // NOTE: always call `done()` here to close
      // the connection to the database
      done();

      return callback(err);
    });
  });

}
