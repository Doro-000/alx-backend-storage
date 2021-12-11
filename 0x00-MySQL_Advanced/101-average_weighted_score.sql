-- creates a stored procedure ComputeAverageWeightedScoreForUsers that computes
-- and store the average weighted score for all students

DELIMITER //
CREATE
  PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
  BEGIN
    DECLARE sum_weight, sum_product_weighted_score INT;
    SET sum_weight = (SELECT SUM(`weight`) FROM projects WHERE id IN (SELECT
      project_id
      FROM corrections
      WHERE corrections.user_id = user_id));
    SET sum_product_weighted_score = (SELECT SUM(`weight` * score) FROM projects LEFT JOIN (corrections)
    ON (id = project_id AND corrections.user_id = user_id));
UPDATE users 
SET 
    average_score = sum_product_weighted_score / sum_weight
WHERE
    id = user_id;
  END	//

DELIMITER ;



DELIMITER //
CREATE
  PROCEDURE ComputeAverageWeightedScoreForUsers ()
  BEGIN
    DECLARE id_holder, weighted_avg INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE id_fetch CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    OPEN id_fetch;
    WHILE NOT done DO
      FETCH id_fetch INTO id_holder;
      CALL ComputeAverageWeightedScoreForUser(id_holder);
    END WHILE;
  END //
DELIMITER ;
