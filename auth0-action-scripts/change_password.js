function changePassword (email, newPassword, callback) {
  //this example uses the "pg" library
  //more info here: https://github.com/brianc/node-postgres

  const { Pool } = require('pg');
  const bcrypt = require('bcrypt');

  process.env.NODE_TLS_REJECT_UNAUTHORIZED=0;
  
  const pool = new Pool({
    connectionString: process.env.AIVEN_DATABASE_URI
    ssl: {
      rejectUnauthorized: false
    }
  });

  pool.connect(function (err, client, done) {
    if (err) return callback(err);

    bcrypt.hash(newPassword, 10, function (err, hash) {
      if (err) return callback(err);

      const query = 'UPDATE public.users_customuser SET password = $1 WHERE email = $2';
      client.query(query, [hash, email], function (err, result) {
        // NOTE: always call `done()` here to close
        // the connection to the database
        done();

        return callback(err, result && result.rowCount > 0);
      });
    });
  });
}
