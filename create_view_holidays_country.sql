CREATE OR REPLACE VIEW holiday.v_holidays_country AS
SELECT c.country_name, h.date
FROM holiday.holidays_country AS h
INNER JOIN holiday.countries AS c
ON h.country_code = c.country_code;