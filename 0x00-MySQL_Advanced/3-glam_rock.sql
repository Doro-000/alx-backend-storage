-- lists all bands with Glam rock as their main style, ranked by their longevity
SELECT
	band_name,
    IF(split IS NULL, YEAR(NOW()) - formed, split - formed) as lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', style) != 0
ORDER BY lifespan DESC;
