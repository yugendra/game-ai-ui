CREATE DATABASE IF NOT EXISTS user_creds;
USE user_creds;
DROP PROCEDURE IF EXISTS init;
DELIMITER //
CREATE PROCEDURE init ()
LANGUAGE SQL
BEGIN
  DECLARE user_exist, data_present INT;
  SET user_exist = (SELECT EXISTS (SELECT DISTINCT user FROM mysql.user WHERE user = "root"));
  IF user_exist = 0 THEN
    CREATE USER 'root'@'localhost' IDENTIFIED BY 'devops123';
    GRANT ALL PRIVILEGES ON user_creds.* TO 'root'@'localhost';
    FLUSH PRIVILEGES;
  END IF;
  CREATE TABLE IF NOT EXISTS user_table (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64),
    password VARCHAR(64),
    container_id VARCHAR(64),
    vnc_port INTEGER(10),
    ssh_port INTEGER(10),
    is_container_running BOOLEAN NOT NULL DEFAULT 0
  );
  SET data_present = (SELECT COUNT(*) FROM user_table);
  IF data_present = 0 THEN
    INSERT INTO user_table (username, password,container_id,vnc_port,ssh_port,is_container_running) VALUES
      ("admin", "devops123","abc","435","123",0);
  END IF;
END;//
DELIMITER ;
CALL init();
