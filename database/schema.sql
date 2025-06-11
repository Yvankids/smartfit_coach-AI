-- Users table
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
) ENGINE=InnoDB;

-- User profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    username VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(100),
    profile_picture LONGBLOB,
    height FLOAT,
    weight FLOAT,
    fitness_goal VARCHAR(50),
    experience_level ENUM('beginner', 'intermediate', 'advanced'),
    target_weight FLOAT,
    FOREIGN KEY (username) REFERENCES users(username)
) ENGINE=InnoDB;

-- Progress tracking table
CREATE TABLE IF NOT EXISTS fitness_progress (
    progress_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    date DATE,
    current_weight FLOAT,
    workout_duration INT,
    calories_burned INT,
    form_score FLOAT,
    notes TEXT,
    FOREIGN KEY (username) REFERENCES users(username)
) ENGINE=InnoDB;