
function create(user, callback) {
  // Auth0 automatically checks for existing user before creating a new user with this script
  
  const { Pool } = require('pg');
  const bcrypt = require('bcrypt');

  process.env.NODE_TLS_REJECT_UNAUTHORIZED=0;
  
  const pool = new Pool({
    connectionString: process.env.AIVEN_DATABASE_URI,
    ssl: {
      rejectUnauthorized: false
    }
  });

  const currentDate = new Date();

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth(); // Note: getMonth() returns 0-11 for Jan-Dec
  const day = currentDate.getDate();

  const is_superuser = false;
  const is_staff = false;
  const is_active = true;
  const date_joined = new Date();
  const image = "https://www.gravatar.com/avatar";
  const first_name = "new";
  const last_name = "user";
  const dob = new Date(year, month, day);
  const telephone = "012345"
  const gender = "PREFER_NOT_TO_SAY";
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

      const query = 'INSERT INTO public.users_customuser(image, email, username, first_name, last_name, dob, telephone, gender, role, password, is_superuser, is_staff, is_active, date_joined, dietary_preference, health_goal, allergens, activity_level, cuisines, medical_conditions, taste_preferences, is_on_boarded, vote_strength, is_verified ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24)';
      client.query(query,
        [
          image,
          user.email,
          user.email.split('@')[0],
          first_name,
          last_name,
          dob,
          telephone,
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
