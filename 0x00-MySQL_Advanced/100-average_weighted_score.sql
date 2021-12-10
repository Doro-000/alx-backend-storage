--stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student

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
