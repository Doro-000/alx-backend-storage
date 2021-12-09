-- creates a stored procedure AddBonus that adds a new correction for a student
DELIMITER //

CREATE
  PROCEDURE AddBonus (IN user_id INT, INOUT project_name VARCHAR(255), IN score INT)
  BEGIN
    IF (SELECT project_name NOT IN (SELECT name FROM projects) = 1)
    THEN
      INSERT INTO projects (name) VALUE (project_name);
      INSERT INTO corrections (user_id, project_id, score)
      VALUES (user_id, (SELECT id FROM projects WHERE name = project_name), score);
    ELSE
      UPDATE corrections SET corrections.score = score
      WHERE corrections.user_id = user_id AND corrections.project_id = (SELECT id FROM projects WHERE name = project_name);
    END IF;
  END //
DELIMITER ;
