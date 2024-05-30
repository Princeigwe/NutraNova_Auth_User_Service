
function create(user, callback) {
  
  const { Pool } = require('pg');
  const bcrypt = require('bcrypt');

  process.env.NODE_TLS_REJECT_UNAUTHORIZED=0;
  
  const pool = new Pool({
    connectionString: 'postgres://avnadmin:AVNS_agDmoS-GaLqBm8gWKfo@nutra-nova-nutra-nova.aivencloud.com:17884/defaultdb?sslmode=require',
    ssl: {
      rejectUnauthorized: false
    }
  });

  const is_superuser = false;
  const is_staff = false;
  const is_active = false;
  const date_joined = new Date();
  const image = "https://www.gravatar.com/avatar";
  const first_name = "new";
  const last_name = "user";
  const age = 12;
  const gender = "MALE";
  const role = "USER";
  const dietary_preference = "GENERAL";
  const health_goal = "IMMUNE_SUPPORT";
  const allergens = "MILK";
  const activity_level = "SEDENTARY";
  const cuisines = "ITALIAN";
  const medical_conditions = "";
  const taste_preferences = "SWEET,SPICY";
  const is_on_boarded = false;
  const vote_strength = 1;
  const is_verified = false


  pool.connect((err, client, done) => {
    if (err) return callback(err);

    bcrypt.hash(user.password, 10, (err, hashedPassword) => {
      if (err) {
        done();
        return callback(err);
      }

      const query = 'INSERT INTO public.users_customuser(image, email, username, first_name, last_name, age, gender, role, password, is_superuser, is_staff, is_active, date_joined, dietary_preference, health_goal, allergens, activity_level, cuisines, medical_conditions, taste_preferences, is_on_boarded, vote_strength, is_verified ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23)';
      client.query(query,
        [
          image,
          user.email,
          user.email.split('@')[0],
          first_name,
          last_name,
          age,
          gender,
          role,
          hashedPassword,
          is_superuser,
          is_staff,
          is_active,
          date_joined,
          dietary_preference,
          health_goal,
          allergens,
          activity_level,
          cuisines,
          medical_conditions,
          taste_preferences,
          is_on_boarded,
          vote_strength,
          is_verified
        ], (err, result) => {
        // Release the client back to the pool
        done();

        return callback(err);
      });
    });
  });
}
