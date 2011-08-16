SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `hunchWorks` ;
CREATE SCHEMA IF NOT EXISTS `hunchWorks` DEFAULT CHARACTER SET latin1 ;
USE `hunchWorks` ;

-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_language`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_language` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_language` (
  `language_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `language_name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`language_id`) ,
  UNIQUE INDEX `name_UNIQUE` (`language_name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_user` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_user` (
  `title` TINYINT UNSIGNED NOT NULL ,
  `show_profile_reminder` TINYINT UNSIGNED NOT NULL ,
  `privacy` TINYINT UNSIGNED NOT NULL ,
  `default_language_id` INT UNSIGNED NOT NULL ,
  `bio_text` TEXT NULL ,
  `phone` VARCHAR(20) NULL ,
  `skype_name` VARCHAR(30) NULL ,
  `website` VARCHAR(100) NULL ,
  `profile_picture` VARCHAR(100) NULL ,
  `screen_name` VARCHAR(45) NULL ,
  `messenger_service` TINYINT UNSIGNED NULL ,
  INDEX `fk_hw_user__language_id` (`default_language_id` ASC) ,
  CONSTRAINT `fk_hw_user__language_id`
    FOREIGN KEY (`default_language_id` )
    REFERENCES `hunchWorks`.`hw_language` (`language_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_location`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_location` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_location` (
  `location_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `location_name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`location_id`) ,
  UNIQUE INDEX `name_UNIQUE` (`location_name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_group` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_group` (
  `group_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(100) NULL ,
  `group_type` TINYINT UNSIGNED NOT NULL ,
  `privacy` TINYINT UNSIGNED NOT NULL ,
  `location_id` INT UNSIGNED NULL ,
  `logo` VARCHAR(100) NULL ,
  PRIMARY KEY (`group_id`) ,
  INDEX `fk_hw_group__location_id` (`location_id` ASC) ,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) ,
  CONSTRAINT `fk_hw_group__location_id`
    FOREIGN KEY (`location_id` )
    REFERENCES `hunchWorks`.`hw_location` (`location_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_organization`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_organization` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_organization` (
  `organization_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(125) NOT NULL ,
  `abbreviation` VARCHAR(7) NOT NULL ,
  `group_id` INT UNSIGNED NOT NULL ,
  `location_id` INT UNSIGNED NULL ,
  PRIMARY KEY (`organization_id`) ,
  INDEX `fk_hw_organization__group_id` (`group_id` ASC) ,
  INDEX `fk_hw_organization__location_id` (`location_id` ASC) ,
  CONSTRAINT `fk_hw_organization__group_id`
    FOREIGN KEY (`group_id` )
    REFERENCES `hunchWorks`.`hw_group` (`group_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_organization__location_id`
    FOREIGN KEY (`location_id` )
    REFERENCES `hunchWorks`.`hw_location` (`location_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_role`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_role` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_role` (
  `role_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `organization_id` INT UNSIGNED NOT NULL ,
  `title` VARCHAR(40) NOT NULL ,
  `start_date` DATE NOT NULL ,
  `end_date` DATE NULL ,
  `description` TEXT NULL ,
  PRIMARY KEY (`role_id`) ,
  INDEX `fk_hw_role__organization_id` (`organization_id` ASC) ,
  CONSTRAINT `fk_hw_role__organization_id`
    FOREIGN KEY (`organization_id` )
    REFERENCES `hunchWorks`.`hw_organization` (`organization_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_user_roles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_user_roles` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_user_roles` (
  `user_id` INT UNSIGNED NOT NULL ,
  `role_id` INT UNSIGNED NOT NULL ,
  INDEX `fk_hw_user_roles__user_id` (`user_id` ASC) ,
  INDEX `fk_hw_user_roles__role_id` (`role_id` ASC) ,
  PRIMARY KEY (`user_id`, `role_id`) ,
  CONSTRAINT `fk_hw_user_roles__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_user_roles__role_id`
    FOREIGN KEY (`role_id` )
    REFERENCES `hunchWorks`.`hw_role` (`role_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_skill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_skill` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_skill` (
  `skill_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `skill_name` VARCHAR(100) NOT NULL ,
  `is_language` TINYINT NOT NULL ,
  `is_technical` TINYINT NOT NULL ,
  PRIMARY KEY (`skill_id`) ,
  UNIQUE INDEX `skill_UNIQUE` (`skill_name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_hunch`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_hunch` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_hunch` (
  `hunch_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `creator_id` INT UNSIGNED NOT NULL ,
  `time_created` DATETIME NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  `title` VARCHAR(100) NOT NULL ,
  `privacy` TINYINT UNSIGNED NOT NULL ,
  `strength` SMALLINT NOT NULL DEFAULT 0 ,
  `language_id` INT UNSIGNED NULL ,
  `location_id` INT UNSIGNED NULL ,
  `description` TEXT NULL ,
  PRIMARY KEY (`hunch_id`) ,
  INDEX `fk_hw_hunch__language_id` (`language_id` ASC) ,
  INDEX `fk_hw_hunch__location_id` (`location_id` ASC) ,
  INDEX `fk_hw_hunch__creator_id` (`creator_id` ASC) ,
  CONSTRAINT `fk_hw_hunch__language_id`
    FOREIGN KEY (`language_id` )
    REFERENCES `hunchWorks`.`hw_language` (`language_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_hunch__location_id`
    FOREIGN KEY (`location_id` )
    REFERENCES `hunchWorks`.`hw_location` (`location_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_hunch__creator_id`
    FOREIGN KEY (`creator_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_education`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_education` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_education` (
  `education_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `school` VARCHAR(255) NOT NULL ,
  `qualification` VARCHAR(100) NOT NULL ,
  `start_date` DATE NOT NULL ,
  `end_date` DATE NULL ,
  PRIMARY KEY (`education_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_class`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_class` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_class` (
  `class_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(45) NOT NULL ,
  `start_date` DATE NOT NULL ,
  `end_date` DATE NULL ,
  PRIMARY KEY (`class_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_education_connections`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_education_connections` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_education_connections` (
  `education_connection_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `education_id` INT UNSIGNED NULL ,
  `class_id` INT UNSIGNED NULL ,
  INDEX `fk_hw_education_connections__user_id` (`user_id` ASC) ,
  INDEX `fk_hw_education_connections__education_id` (`education_id` ASC) ,
  PRIMARY KEY (`education_connection_id`) ,
  INDEX `fk_hw_education_connections__class_id` (`class_id` ASC) ,
  CONSTRAINT `fk_hw_education_connections__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_education_connections__education_id`
    FOREIGN KEY (`education_id` )
    REFERENCES `hunchWorks`.`hw_education` (`education_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_education_connections__class_id`
    FOREIGN KEY (`class_id` )
    REFERENCES `hunchWorks`.`hw_class` (`class_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_skill_connections`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_skill_connections` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_skill_connections` (
  `skill_connection_id` INT UNSIGNED NOT NULL ,
  `skill_id` INT UNSIGNED NOT NULL ,
  `level` TINYINT UNSIGNED NOT NULL ,
  `hunch_id` INT UNSIGNED NULL ,
  `user_id` INT UNSIGNED NULL ,
  INDEX `fk_hw_skill_connections__hunch_id` (`hunch_id` ASC) ,
  INDEX `fk_hw_skill_connections__skill_id` (`skill_id` ASC) ,
  PRIMARY KEY (`skill_connection_id`) ,
  INDEX `fk_hw_skill_connections__user_id` (`user_id` ASC) ,
  CONSTRAINT `fk_hw_skill_connections__hunch_id`
    FOREIGN KEY (`hunch_id` )
    REFERENCES `hunchWorks`.`hw_hunch` (`hunch_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_skill_connections__skill_id`
    FOREIGN KEY (`skill_id` )
    REFERENCES `hunchWorks`.`hw_skill` (`skill_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_skill_connections__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_human_connections`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_human_connections` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_human_connections` (
  `human_connection_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `access_level` TINYINT UNSIGNED NOT NULL ,
  `trust_from_user` TINYINT UNSIGNED NOT NULL ,
  `trust_from_group` TINYINT UNSIGNED NOT NULL ,
  `receive_updates` TINYINT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  `group_id` INT UNSIGNED NULL ,
  `other_user_id` INT UNSIGNED NULL ,
  INDEX `fk_hw_human_connections__group_id` (`group_id` ASC) ,
  INDEX `fk_hw_human_connections__user` (`user_id` ASC) ,
  PRIMARY KEY (`human_connection_id`) ,
  INDEX `fk_hw_human_connections__other_user_id` (`other_user_id` ASC) ,
  CONSTRAINT `fk_hw_human_connections__group_id`
    FOREIGN KEY (`group_id` )
    REFERENCES `hunchWorks`.`hw_group` (`group_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_human_connections__user`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_human_connections__other_user_id`
    FOREIGN KEY (`other_user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_evidence`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_evidence` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_evidence` (
  `evidence_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `hunch_id` INT UNSIGNED NOT NULL ,
  `creator_id` INT UNSIGNED NOT NULL ,
  `strength` SMALLINT NOT NULL DEFAULT 0 ,
  `time_created` DATETIME NOT NULL ,
  `description` TEXT NULL ,
  INDEX `fk_hw_evidence__hunch_id` (`hunch_id` ASC) ,
  INDEX `fk_hw_evidence__creator_id` (`creator_id` ASC) ,
  PRIMARY KEY (`evidence_id`) ,
  CONSTRAINT `fk_hw_evidence__hunch_id`
    FOREIGN KEY (`hunch_id` )
    REFERENCES `hunchWorks`.`hw_hunch` (`hunch_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_evidence__creator_id`
    FOREIGN KEY (`creator_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_attachment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_attachment` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_attachment` (
  `attachment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `attachment_type` TINYINT UNSIGNED NOT NULL ,
  `file_location` VARCHAR(100) NOT NULL ,
  PRIMARY KEY (`attachment_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_evidence_attachments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_evidence_attachments` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_evidence_attachments` (
  `attachment_id` INT UNSIGNED NOT NULL ,
  `evidence_id` INT UNSIGNED NOT NULL ,
  INDEX `fk_hw_evidence_attachments__attachment_id` (`attachment_id` ASC) ,
  PRIMARY KEY (`attachment_id`, `evidence_id`) ,
  INDEX `fk_hw_evidence_attachment__evidence_id` (`evidence_id` ASC) ,
  CONSTRAINT `fk_hw_evidence_attachments__attachment_id`
    FOREIGN KEY (`attachment_id` )
    REFERENCES `hunchWorks`.`hw_attachment` (`attachment_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_evidence_attachment__evidence_id`
    FOREIGN KEY (`evidence_id` )
    REFERENCES `hunchWorks`.`hw_evidence` (`evidence_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_album`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_album` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_album` (
  `album_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`album_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_invited_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_invited_user` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_invited_user` (
  `email` VARCHAR(45) NOT NULL ,
  `user_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`email`) ,
  INDEX `fk_hw_invited_user__user_id` (`user_id` ASC) ,
  CONSTRAINT `fk_hw_invited_user__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_hunch_connections`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_hunch_connections` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_hunch_connections` (
  `hunch_connection_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `hunch_id` INT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  `user_id` INT UNSIGNED NULL ,
  `group_id` INT UNSIGNED NULL ,
  `invited_email` VARCHAR(45) NULL ,
  INDEX `fk_hw_hunch_connections__hunch_id` (`hunch_id` ASC) ,
  INDEX `fk_hw_hunch_connections__user_id` (`user_id` ASC) ,
  PRIMARY KEY (`hunch_connection_id`) ,
  INDEX `fk_hw_hunch_connections__group_id` (`group_id` ASC) ,
  INDEX `fk_hw_hunch_connections__invited_email` (`invited_email` ASC) ,
  CONSTRAINT `fk_hw_hunch_connections__hunch_id`
    FOREIGN KEY (`hunch_id` )
    REFERENCES `hunchWorks`.`hw_hunch` (`hunch_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_hunch_connections__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_hunch_connections__group_id`
    FOREIGN KEY (`group_id` )
    REFERENCES `hunchWorks`.`hw_group` (`group_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_hunch_connections__invited_email`
    FOREIGN KEY (`invited_email` )
    REFERENCES `hunchWorks`.`hw_invited_user` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_user_invites`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_user_invites` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_user_invites` (
  `user_id` INT UNSIGNED NOT NULL ,
  `invited_email` VARCHAR(45) NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  INDEX `fk_hw_user_invites__user_id` (`user_id` ASC) ,
  INDEX `fk_hw_user_invites__invited_email` (`invited_email` ASC) ,
  PRIMARY KEY (`user_id`, `invited_email`) ,
  CONSTRAINT `fk_hw_user_invites__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_user_invites__invited_email`
    FOREIGN KEY (`invited_email` )
    REFERENCES `hunchWorks`.`hw_invited_user` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_location_interests`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_location_interests` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_location_interests` (
  `user_id` INT UNSIGNED NOT NULL ,
  `location_id` INT UNSIGNED NOT NULL ,
  INDEX `fk_hw_location_interests__user_id` (`user_id` ASC) ,
  INDEX `fk_hw_location_interests__location_id` (`location_id` ASC) ,
  PRIMARY KEY (`user_id`, `location_id`) ,
  CONSTRAINT `fk_hw_location_interests__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_location_interests__location_id`
    FOREIGN KEY (`location_id` )
    REFERENCES `hunchWorks`.`hw_location` (`location_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_evidence_albums`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_evidence_albums` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_evidence_albums` (
  `album_id` INT UNSIGNED NOT NULL ,
  `evidence_id` INT UNSIGNED NOT NULL ,
  INDEX `fk_hw_evidence_albums__album_id` (`album_id` ASC) ,
  PRIMARY KEY (`album_id`, `evidence_id`) ,
  INDEX `fk_hw_evidence_albums__evidence_id` (`evidence_id` ASC) ,
  CONSTRAINT `fk_hw_evidence_albums__album_id`
    FOREIGN KEY (`album_id` )
    REFERENCES `hunchWorks`.`hw_album` (`album_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_evidence_albums__evidence_id`
    FOREIGN KEY (`evidence_id` )
    REFERENCES `hunchWorks`.`hw_evidence` (`evidence_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_album_attachments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_album_attachments` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_album_attachments` (
  `album_id` INT UNSIGNED NOT NULL ,
  `attachment_id` INT UNSIGNED NOT NULL ,
  INDEX `fk_hw_album_attachments__album_id` (`album_id` ASC) ,
  INDEX `fk_hw_album_attachments__attachment_id` (`attachment_id` ASC) ,
  PRIMARY KEY (`album_id`, `attachment_id`) ,
  CONSTRAINT `fk_hw_album_attachments__album_id`
    FOREIGN KEY (`album_id` )
    REFERENCES `hunchWorks`.`hw_album` (`album_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_album_attachments__attachment_id`
    FOREIGN KEY (`attachment_id` )
    REFERENCES `hunchWorks`.`hw_attachment` (`attachment_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_tag`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_tag` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_tag` (
  `tag_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `tag_name` VARCHAR(30) NOT NULL ,
  PRIMARY KEY (`tag_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_tag_connections`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_tag_connections` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_tag_connections` (
  `tag_connections_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `hunch_id` INT UNSIGNED NULL ,
  `tag_id` INT UNSIGNED NOT NULL ,
  `evidence_id` INT UNSIGNED NULL ,
  PRIMARY KEY (`tag_connections_id`) ,
  INDEX `fk_hw_tag_connections__hunch_id` () ,
  INDEX `fk_hw_tag_connections__evidence_id` () ,
  INDEX `fk_hw_tag_connections__tag_id` () ,
  CONSTRAINT `fk_hw_tag_connections__hunch_id`
    FOREIGN KEY ()
    REFERENCES `hunchWorks`.`hw_hunch` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_tag_connections__evidence_id`
    FOREIGN KEY ()
    REFERENCES `hunchWorks`.`hw_evidence` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_tag_connections__tag_id`
    FOREIGN KEY ()
    REFERENCES `hunchWorks`.`hw_tag` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
