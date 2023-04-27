dict = {"NV":"Nevada", 
        "TX": "Texas", 
        "IN": "Indianapolis",
        "CA":"California", 
        "VA":"Virgina", 
        "NY":"New York", 
        "ND": "North Dakota", 
        "MI":"Michigan",
        "GA": "Georgia",
        "New York, NY": "New York",
        "Ciudad Autónoma de Buenos Aires": "Buenos Aires"}

table_countries = '''
CREATE TABLE IF NOT EXISTS `uni_countries`.`countries` (
  `idstate` INT NOT NULL AUTO_INCREMENT,
  `country`VARCHAR(45),
  `state_province` VARCHAR(45),
  `latitude` DECIMAL,
  `longitude`DECIMAL,
  PRIMARY KEY (`idstate`))
ENGINE = InnoDB;
'''

table_universities = '''
CREATE TABLE IF NOT EXISTS `uni_countries`.`universities` (
  `iduniversities` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100),
  `web_page` VARCHAR(100),
  `idstate` INT,
  PRIMARY KEY (`iduniversities`),
  CONSTRAINT `countries_idstate`
    FOREIGN KEY (`idstate`)
    REFERENCES `uni_countries`.`countries`(`idstate`))
ENGINE = InnoDB;
'''

querys_list = [table_countries, table_universities]