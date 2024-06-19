-- creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users
    SET average_score = (
        SELECT SUM(score * weight) / SUM(weight) AS w_avg
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE users.id = corrections.user_id
        GROUP BY corrections.user_id
    );
END //
DELIMITER ;
