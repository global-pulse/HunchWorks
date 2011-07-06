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
  `name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`language_id`) ,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_user_messenger`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_user_messenger` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_user_messenger` (
  `user_messenger_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `screen_name` VARCHAR(45) NOT NULL ,
  `messenger_service` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_messenger_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_user` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_user` (
  `user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `email` VARCHAR(45) NOT NULL ,
  `first_name` VARCHAR(25) NOT NULL ,
  `last_name` VARCHAR(50) NOT NULL ,
  `title` TINYINT UNSIGNED NOT NULL ,
  `bio_text` TEXT NULL ,
  `work_phone` VARCHAR(30) NULL ,
  `skype_name` VARCHAR(30) NULL ,
  `instant_messenger_id` INT UNSIGNED NULL ,
  `website` VARCHAR(100) NULL ,
  `profile_picture` VARCHAR(100) NULL ,
  `show_profile_reminder` TINYINT UNSIGNED NOT NULL ,
  `privacy` TINYINT UNSIGNED NOT NULL ,
  `default_language_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_id`) ,
  INDEX `fk_hw_user__language_id` (`default_language_id` ASC) ,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) ,
  INDEX `fk_hw_user__instant_messenger_id` (`instant_messenger_id` ASC) ,
  CONSTRAINT `fk_hw_user__language_id`
    FOREIGN KEY (`default_language_id` )
    REFERENCES `hunchWorks`.`hw_language` (`language_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_user__instant_messenger_id`
    FOREIGN KEY (`instant_messenger_id` )
    REFERENCES `hunchWorks`.`hw_user_messenger` (`user_messenger_id` )
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
  `name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`location_id`) ,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) )
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
  `abbreviation` VARCHAR(15) NOT NULL ,
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
  `title` VARCHAR(255) NOT NULL ,
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
  `user_role_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `role_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_role_id`) ,
  INDEX `fk_hw_user_roles__user_id` (`user_id` ASC) ,
  INDEX `fk_hw_user_roles__role_id` (`role_id` ASC) ,
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
-- Table `hunchWorks`.`hw_user_connections`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_user_connections` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_user_connections` (
  `user_connection_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_a_id` INT UNSIGNED NOT NULL ,
  `user_b_id` INT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_connection_id`) ,
  INDEX `fk_hw_user_connections__user_a_id` (`user_a_id` ASC) ,
  INDEX `fk_hw_user_connections__user_b_id` (`user_b_id` ASC) ,
  CONSTRAINT `fk_hw_user_connections__user_a_id`
    FOREIGN KEY (`user_a_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_user_connections__user_b_id`
    FOREIGN KEY (`user_b_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_skill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_skill` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_skill` (
  `skill_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `skill` VARCHAR(100) NOT NULL ,
  `is_language` TINYINT NOT NULL ,
  `is_technical` TINYINT NOT NULL ,
  PRIMARY KEY (`skill_id`) ,
  UNIQUE INDEX `skill_UNIQUE` (`skill` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_hunch`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_hunch` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_hunch` (
  `hunch_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `time_created` DATETIME NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  `title` VARCHAR(100) NOT NULL ,
  `privacy` TINYINT UNSIGNED NOT NULL ,
  `language_id` INT UNSIGNED NULL ,
  `location_id` INT UNSIGNED NULL ,
  `description` TEXT NULL ,
  `creator_id` INT UNSIGNED NOT NULL ,
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
-- Table `hunchWorks`.`hw_user_education`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_user_education` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_user_education` (
  `user_education_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `education_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_education_id`) ,
  INDEX `fk_hw_user_education__user_id` (`user_id` ASC) ,
  INDEX `fk_hw_user_education__education_id` (`education_id` ASC) ,
  CONSTRAINT `fk_hw_user_education__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_user_education__education_id`
    FOREIGN KEY (`education_id` )
    REFERENCES `hunchWorks`.`hw_education` (`education_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_user_skills`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_user_skills` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_user_skills` (
  `user_skill_id` INT UNSIGNED NOT NULL ,
  `user_id` INT UNSIGNED NOT NULL ,
  `skill_id` INT UNSIGNED NOT NULL ,
  `level` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_skill_id`) ,
  INDEX `fk_hw_user_skills__user_id` (`user_id` ASC) ,
  INDEX `fk_hw_user_skills__skill_id` (`skill_id` ASC) ,
  CONSTRAINT `fk_hw_user_skills__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_user_skills__skill_id`
    FOREIGN KEY (`skill_id` )
    REFERENCES `hunchWorks`.`hw_skill` (`skill_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_hunch_skills`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_hunch_skills` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_hunch_skills` (
  `hunch_skill_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `hunch_id` INT UNSIGNED NOT NULL ,
  `skill_id` INT UNSIGNED NOT NULL ,
  `level` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`hunch_skill_id`) ,
  INDEX `fk_hw_hunch_skills__hunch_id` (`hunch_id` ASC) ,
  INDEX `fk_hw_hunch_skills__skill_id` (`skill_id` ASC) ,
  CONSTRAINT `fk_hw_hunch_skills__hunch_id`
    FOREIGN KEY (`hunch_id` )
    REFERENCES `hunchWorks`.`hw_hunch` (`hunch_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_hunch_skills__skill_id`
    FOREIGN KEY (`skill_id` )
    REFERENCES `hunchWorks`.`hw_skill` (`skill_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_group_connections`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_group_connections` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_group_connections` (
  `group_user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `group_id` INT UNSIGNED NOT NULL ,
  `access_level` TINYINT UNSIGNED NOT NULL ,
  `trust_from_user` INT UNSIGNED NOT NULL ,
  `trust_from_group` INT UNSIGNED NOT NULL ,
  `receive_updates` TINYINT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`group_user_id`) ,
  INDEX `fk_hw_group_connections__group_id` (`group_id` ASC) ,
  INDEX `fk_hw_group_connections__user` (`user_id` ASC) ,
  CONSTRAINT `fk_hw_group_connections__group_id`
    FOREIGN KEY (`group_id` )
    REFERENCES `hunchWorks`.`hw_group` (`group_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_group_connections__user`
    FOREIGN KEY (`user_id` )
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
  `time_created` DATETIME NOT NULL ,
  `description` TEXT NULL ,
  PRIMARY KEY (`evidence_id`) ,
  INDEX `fk_hw_evidence__hunch_id` (`hunch_id` ASC) ,
  INDEX `fk_hw_evidence__creator_id` (`creator_id` ASC) ,
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
-- Table `hunchWorks`.`hw_hunch_groups`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_hunch_groups` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_hunch_groups` (
  `hunch_groups_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `group_id` INT UNSIGNED NOT NULL ,
  `hunch_id` INT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`hunch_groups_id`) ,
  INDEX `fk_hw_hunch_groups__group_id` (`group_id` ASC) ,
  INDEX `fk_hw_hunch_groups__hunch_id` (`hunch_id` ASC) ,
  CONSTRAINT `fk_hw_hunch_groups__group_id`
    FOREIGN KEY (`group_id` )
    REFERENCES `hunchWorks`.`hw_group` (`group_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_hunch_groups__hunch_id`
    FOREIGN KEY (`hunch_id` )
    REFERENCES `hunchWorks`.`hw_hunch` (`hunch_id` )
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
  `file_location` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`attachment_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_evidence_attachments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_evidence_attachments` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_evidence_attachments` (
  `evidence_attachment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `attachment_id` INT UNSIGNED NOT NULL ,
  `evidence_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`evidence_attachment_id`) ,
  INDEX `fk_hw_evidence_attachments__attachment_id` (`attachment_id` ASC) ,
  INDEX `fk_hw_evidence_attachments__evidence_id` (`evidence_id` ASC) ,
  CONSTRAINT `fk_hw_evidence_attachments__attachment_id`
    FOREIGN KEY (`attachment_id` )
    REFERENCES `hunchWorks`.`hw_attachment` (`attachment_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_evidence_attachments__evidence_id`
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
-- Table `hunchWorks`.`hw_hunch_connections`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_hunch_connections` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_hunch_connections` (
  `hunch_connections_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `hunch_id` INT UNSIGNED NOT NULL ,
  `user_id` INT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`hunch_connections_id`) ,
  INDEX `fk_hw_hunch_connections__hunch_id` (`hunch_id` ASC) ,
  INDEX `fk_hw_hunch_connections__user_id` (`user_id` ASC) ,
  CONSTRAINT `fk_hw_hunch_connections__hunch_id`
    FOREIGN KEY (`hunch_id` )
    REFERENCES `hunchWorks`.`hw_hunch` (`hunch_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_hunch_connections__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_invited_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_invited_user` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_invited_user` (
  `invited_users_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NULL ,
  `email` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`invited_users_id`) ,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) ,
  INDEX `fk_hw_invited_users__user_id` (`user_id` ASC) ,
  CONSTRAINT `fk_hw_invited_users__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_hunch_invites`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_hunch_invites` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_hunch_invites` (
  `hunch_invites_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `invited_user_id` INT UNSIGNED NOT NULL ,
  `hunch_id` INT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`hunch_invites_id`) ,
  INDEX `fk_hw_hunch_invites__invited_user_id` (`invited_user_id` ASC) ,
  INDEX `fk_hw_hunch_invites__hunch_id` (`hunch_id` ASC) ,
  CONSTRAINT `fk_hw_hunch_invites__invited_user_id`
    FOREIGN KEY (`invited_user_id` )
    REFERENCES `hunchWorks`.`hw_invited_user` (`invited_users_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_hunch_invites__hunch_id`
    FOREIGN KEY (`hunch_id` )
    REFERENCES `hunchWorks`.`hw_hunch` (`hunch_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_user_invites`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_user_invites` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_user_invites` (
  `user_invites_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `invited_users_id` INT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_invites_id`) ,
  INDEX `fk_hw_user_invites__invited_user_id` (`invited_users_id` ASC) ,
  INDEX `fk_hw_user_invites__user_id` (`user_id` ASC) ,
  CONSTRAINT `fk_hw_user_invites__invited_user_id`
    FOREIGN KEY (`invited_users_id` )
    REFERENCES `hunchWorks`.`hw_invited_user` (`invited_users_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_user_invites__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`hw_location_interests`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_location_interests` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_location_interests` (
  `location_interests_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `location_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`location_interests_id`) ,
  INDEX `fk_hw_location_interests__user_id` (`user_id` ASC) ,
  INDEX `fk_hw_location_interests__location_id` (`location_id` ASC) ,
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
  `evidence_albums_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `album_id` INT UNSIGNED NOT NULL ,
  `evidence_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`evidence_albums_id`) ,
  INDEX `fk_hw_evidence_albums__album_id` (`album_id` ASC) ,
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
  `album_attachments_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `album_id` INT UNSIGNED NOT NULL ,
  `attachment_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`album_attachments_id`) ,
  INDEX `fk_hw_album_attachments__album_id` (`album_id` ASC) ,
  INDEX `fk_hw_album_attachments__attachment_id` (`attachment_id` ASC) ,
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
-- Table `hunchWorks`.`hw_user_classes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`hw_user_classes` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`hw_user_classes` (
  `user_class_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `class_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_class_id`) ,
  INDEX `fk_hw_user_classes_user_id` (`user_id` ASC) ,
  INDEX `fk_hw_user_classes_class_id` (`class_id` ASC) ,
  CONSTRAINT `fk_hw_user_classes_user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`hw_user` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hw_user_classes_class_id`
    FOREIGN KEY (`class_id` )
    REFERENCES `hunchWorks`.`hw_class` (`class_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
