SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `hunchWorks` ;
CREATE SCHEMA IF NOT EXISTS `hunchWorks` DEFAULT CHARACTER SET latin1 ;
USE `hunchWorks` ;

-- -----------------------------------------------------
-- Table `hunchWorks`.`Language`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`Language` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`Language` (
  `language_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`language_id`) ,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`UserInstantMessenger`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`UserInstantMessenger` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`UserInstantMessenger` (
  `user_messenger_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `screen_name` VARCHAR(45) NOT NULL ,
  `messenger_service` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_messenger_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`User` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`User` (
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
  INDEX `fk_User__language_id` (`default_language_id` ASC) ,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) ,
  INDEX `fk_User__instant_messenger_id` (`instant_messenger_id` ASC) ,
  CONSTRAINT `fk_User__language_id`
    FOREIGN KEY (`default_language_id` )
    REFERENCES `hunchWorks`.`Language` (`language_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_User__instant_messenger_id`
    FOREIGN KEY (`instant_messenger_id` )
    REFERENCES `hunchWorks`.`UserInstantMessenger` (`user_messenger_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `hunchWorks`.`Location`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`Location` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`Location` (
  `location_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`location_id`) ,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`Group`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`Group` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`Group` (
  `group_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(100) NULL ,
  `group_type` TINYINT UNSIGNED NOT NULL ,
  `privacy` TINYINT UNSIGNED NOT NULL ,
  `location_id` INT UNSIGNED NULL ,
  `logo` VARCHAR(100) NULL ,
  PRIMARY KEY (`group_id`) ,
  INDEX `fk_Group__location_id` (`location_id` ASC) ,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) ,
  CONSTRAINT `fk_Group__location_id`
    FOREIGN KEY (`location_id` )
    REFERENCES `hunchWorks`.`Location` (`location_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`Organization`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`Organization` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`Organization` (
  `organization_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(125) NOT NULL ,
  `abbreviation` VARCHAR(15) NOT NULL ,
  `group_id` INT UNSIGNED NOT NULL ,
  `location_id` INT UNSIGNED NULL ,
  PRIMARY KEY (`organization_id`) ,
  INDEX `fk_Organization__group_id` (`group_id` ASC) ,
  INDEX `fk_Organization__location_id` (`location_id` ASC) ,
  CONSTRAINT `fk_Organization__group_id`
    FOREIGN KEY (`group_id` )
    REFERENCES `hunchWorks`.`Group` (`group_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Organization__location_id`
    FOREIGN KEY (`location_id` )
    REFERENCES `hunchWorks`.`Location` (`location_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`Role`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`Role` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`Role` (
  `role_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `organization_id` INT UNSIGNED NOT NULL ,
  `title` VARCHAR(255) NOT NULL ,
  `started` DATE NOT NULL ,
  `ended` DATE NULL ,
  `description` TEXT NULL ,
  PRIMARY KEY (`role_id`) ,
  INDEX `fk_Role__organization_id` (`organization_id` ASC) ,
  CONSTRAINT `fk_Role__organization_id`
    FOREIGN KEY (`organization_id` )
    REFERENCES `hunchWorks`.`Organization` (`organization_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`UserRole`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`UserRole` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`UserRole` (
  `user_role_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `role_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_role_id`) ,
  INDEX `fk_UserRole__user_id` (`user_id` ASC) ,
  INDEX `fk_UserRole__role_id` (`role_id` ASC) ,
  CONSTRAINT `fk_UserRole__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`User` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_UserRole__role_id`
    FOREIGN KEY (`role_id` )
    REFERENCES `hunchWorks`.`Role` (`role_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`UserConnection`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`UserConnection` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`UserConnection` (
  `user_connection_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_a_id` INT UNSIGNED NOT NULL ,
  `user_b_id` INT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_connection_id`) ,
  INDEX `fk_UserConnections__user_a_id` (`user_a_id` ASC) ,
  INDEX `fk_UserConnections__user_b_id` (`user_b_id` ASC) ,
  CONSTRAINT `fk_UserConnections__user_a_id`
    FOREIGN KEY (`user_a_id` )
    REFERENCES `hunchWorks`.`User` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_UserConnections__user_b_id`
    FOREIGN KEY (`user_b_id` )
    REFERENCES `hunchWorks`.`User` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`Skill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`Skill` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`Skill` (
  `skill_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `skill` VARCHAR(100) NOT NULL ,
  `is_language` TINYINT NOT NULL ,
  `is_technical` TINYINT NOT NULL ,
  PRIMARY KEY (`skill_id`) ,
  UNIQUE INDEX `skill_UNIQUE` (`skill` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`Hunch`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`Hunch` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`Hunch` (
  `hunch_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `time_created` DATETIME NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  `title` VARCHAR(100) NOT NULL ,
  `privacy` TINYINT UNSIGNED NOT NULL ,
  `language_id` INT UNSIGNED NULL ,
  `location_id` INT UNSIGNED NULL ,
  `description` TEXT NULL ,
  PRIMARY KEY (`hunch_id`) ,
  INDEX `fk_Hunch__language_id` (`language_id` ASC) ,
  INDEX `fk_Hunch__location_id` (`location_id` ASC) ,
  CONSTRAINT `fk_Hunch__language_id`
    FOREIGN KEY (`language_id` )
    REFERENCES `hunchWorks`.`Language` (`language_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Hunch__location_id`
    FOREIGN KEY (`location_id` )
    REFERENCES `hunchWorks`.`Location` (`location_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`Education`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`Education` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`Education` (
  `education_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `school` VARCHAR(255) NOT NULL ,
  `qualification` VARCHAR(100) NOT NULL ,
  `start_date` DATE NOT NULL ,
  `end_date` DATE NULL ,
  PRIMARY KEY (`education_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`UserEducation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`UserEducation` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`UserEducation` (
  `user_education_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `education_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_education_id`) ,
  INDEX `fk_UserEducation__user_id` (`user_id` ASC) ,
  INDEX `fk_UserEducation__education_id` (`education_id` ASC) ,
  CONSTRAINT `fk_UserEducation__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`User` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_UserEducation__education_id`
    FOREIGN KEY (`education_id` )
    REFERENCES `hunchWorks`.`Education` (`education_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`UserSkills`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`UserSkills` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`UserSkills` (
  `user_skill_Id` INT UNSIGNED NOT NULL ,
  `user_id` INT UNSIGNED NOT NULL ,
  `skill_id` INT UNSIGNED NOT NULL ,
  `level` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_skill_Id`) ,
  INDEX `fk_UserSkills__user_id` (`user_id` ASC) ,
  INDEX `fk_UserSkills__skill_id` (`skill_id` ASC) ,
  CONSTRAINT `fk_UserSkills__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`User` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_UserSkills__skill_id`
    FOREIGN KEY (`skill_id` )
    REFERENCES `hunchWorks`.`Skill` (`skill_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`HunchSkill`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`HunchSkill` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`HunchSkill` (
  `hunch_skill_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `hunch_id` INT UNSIGNED NOT NULL ,
  `skill_id` INT UNSIGNED NOT NULL ,
  `level` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`hunch_skill_id`) ,
  INDEX `fk_HunchSkills__hunch_id` (`hunch_id` ASC) ,
  INDEX `fk_HunchSkills__skill_id` (`skill_id` ASC) ,
  CONSTRAINT `fk_HunchSkills__hunch_id`
    FOREIGN KEY (`hunch_id` )
    REFERENCES `hunchWorks`.`Hunch` (`hunch_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_HunchSkills__skill_id`
    FOREIGN KEY (`skill_id` )
    REFERENCES `hunchWorks`.`Skill` (`skill_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`GroupConnection`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`GroupConnection` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`GroupConnection` (
  `group_user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `group_id` INT UNSIGNED NOT NULL ,
  `access_level` TINYINT UNSIGNED NOT NULL ,
  `trust_from_user` INT UNSIGNED NOT NULL ,
  `trust_from_group` INT UNSIGNED NOT NULL ,
  `receive_updates` TINYINT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`group_user_id`) ,
  INDEX `fk_GroupConnections__group_id` (`group_id` ASC) ,
  INDEX `fk_GroupConnections__user` (`user_id` ASC) ,
  CONSTRAINT `fk_GroupConnections__group_id`
    FOREIGN KEY (`group_id` )
    REFERENCES `hunchWorks`.`Group` (`group_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_GroupConnections__user`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`User` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`Evidence`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`Evidence` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`Evidence` (
  `evidence_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `hunch_id` INT UNSIGNED NOT NULL ,
  `creator_id` INT UNSIGNED NOT NULL ,
  `time_created` DATETIME NOT NULL ,
  `description` TEXT NULL ,
  PRIMARY KEY (`evidence_id`) ,
  INDEX `fk_Evidence__hunch_id` (`hunch_id` ASC) ,
  INDEX `fk_Evidence__creator_id` (`creator_id` ASC) ,
  CONSTRAINT `fk_Evidence__hunch_id`
    FOREIGN KEY (`hunch_id` )
    REFERENCES `hunchWorks`.`Hunch` (`hunch_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Evidence__creator_id`
    FOREIGN KEY (`creator_id` )
    REFERENCES `hunchWorks`.`User` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`HunchGroup`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`HunchGroup` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`HunchGroup` (
  `hunch_groups_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `group_id` INT UNSIGNED NOT NULL ,
  `hunch_id` INT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`hunch_groups_id`) ,
  INDEX `fk_HunchGroups__group_id` (`group_id` ASC) ,
  INDEX `fk_HunchGroups__hunch_id` (`hunch_id` ASC) ,
  CONSTRAINT `fk_HunchGroups__group_id`
    FOREIGN KEY (`group_id` )
    REFERENCES `hunchWorks`.`Group` (`group_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_HunchGroups__hunch_id`
    FOREIGN KEY (`hunch_id` )
    REFERENCES `hunchWorks`.`Hunch` (`hunch_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`Attachment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`Attachment` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`Attachment` (
  `attachment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `attachment_type` TINYINT UNSIGNED NOT NULL ,
  `file_location` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`attachment_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`EvidenceAttachment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`EvidenceAttachment` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`EvidenceAttachment` (
  `evidence_attachment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `attachment_id` INT UNSIGNED NOT NULL ,
  `evidence_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`evidence_attachment_id`) ,
  INDEX `fk_EvidenceAttachment__attachment_id` (`attachment_id` ASC) ,
  INDEX `fk_EvidenceAttachment__evidence_id` (`evidence_id` ASC) ,
  CONSTRAINT `fk_EvidenceAttachment__attachment_id`
    FOREIGN KEY (`attachment_id` )
    REFERENCES `hunchWorks`.`Attachment` (`attachment_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_EvidenceAttachment__evidence_id`
    FOREIGN KEY (`evidence_id` )
    REFERENCES `hunchWorks`.`Evidence` (`evidence_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`Album`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`Album` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`Album` (
  `album_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`album_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`HunchConnection`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`HunchConnection` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`HunchConnection` (
  `hunch_connections_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `hunch_id` INT UNSIGNED NOT NULL ,
  `user_id` INT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`hunch_connections_id`) ,
  INDEX `fk_hunchworks_hunch_connections__hunch_id` (`hunch_id` ASC) ,
  INDEX `fk_hunchworks_hunch_connections__user_id` (`user_id` ASC) ,
  CONSTRAINT `fk_hunchworks_hunch_connections__hunch_id`
    FOREIGN KEY (`hunch_id` )
    REFERENCES `hunchWorks`.`Hunch` (`hunch_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_hunchworks_hunch_connections__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`User` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`InvitedUser`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`InvitedUser` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`InvitedUser` (
  `invited_users_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NULL ,
  `email` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`invited_users_id`) ,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) ,
  INDEX `fk_invitedUsers__user_id` (`user_id` ASC) ,
  CONSTRAINT `fk_invitedUsers__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`User` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`HunchInvites`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`HunchInvites` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`HunchInvites` (
  `hunch_invites_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `invited_user_id` INT UNSIGNED NOT NULL ,
  `hunch_id` INT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`hunch_invites_id`) ,
  INDEX `fk_HunchInvites__invited_user_id` (`invited_user_id` ASC) ,
  INDEX `fk_HunchInvites__hunch_id` (`hunch_id` ASC) ,
  CONSTRAINT `fk_HunchInvites__invited_user_id`
    FOREIGN KEY (`invited_user_id` )
    REFERENCES `hunchWorks`.`InvitedUser` (`invited_users_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_HunchInvites__hunch_id`
    FOREIGN KEY (`hunch_id` )
    REFERENCES `hunchWorks`.`Hunch` (`hunch_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`UserInvite`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`UserInvite` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`UserInvite` (
  `user_invites_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `invited_users_id` INT UNSIGNED NOT NULL ,
  `status` TINYINT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_invites_id`) ,
  INDEX `fk_UserInvites__invited_user_id` (`invited_users_id` ASC) ,
  INDEX `fk_UserInvites__user_id` (`user_id` ASC) ,
  CONSTRAINT `fk_UserInvites__invited_user_id`
    FOREIGN KEY (`invited_users_id` )
    REFERENCES `hunchWorks`.`InvitedUser` (`invited_users_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_UserInvites__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`User` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`LocationInterest`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`LocationInterest` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`LocationInterest` (
  `location_interests_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `location_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`location_interests_id`) ,
  INDEX `fk_LocationInterests__user_id` (`user_id` ASC) ,
  INDEX `fk_LocationInterests__location_id` (`location_id` ASC) ,
  CONSTRAINT `fk_LocationInterests__user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`User` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_LocationInterests__location_id`
    FOREIGN KEY (`location_id` )
    REFERENCES `hunchWorks`.`Location` (`location_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`EvidenceAlbum`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`EvidenceAlbum` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`EvidenceAlbum` (
  `evidence_albums_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `album_id` INT UNSIGNED NOT NULL ,
  `evidence_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`evidence_albums_id`) ,
  INDEX `fk_EvidenceAlbums__album_id` (`album_id` ASC) ,
  INDEX `fk_EvidenceAlbums__evidence_id` (`evidence_id` ASC) ,
  CONSTRAINT `fk_EvidenceAlbums__album_id`
    FOREIGN KEY (`album_id` )
    REFERENCES `hunchWorks`.`Album` (`album_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_EvidenceAlbums__evidence_id`
    FOREIGN KEY (`evidence_id` )
    REFERENCES `hunchWorks`.`Evidence` (`evidence_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`AlbumAttachment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`AlbumAttachment` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`AlbumAttachment` (
  `album_attachments_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `album_id` INT UNSIGNED NOT NULL ,
  `attachment_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`album_attachments_id`) ,
  INDEX `fk_AlbumAttachments__album_id` (`album_id` ASC) ,
  INDEX `fk_AlbumAttachments__attachment_id` (`attachment_id` ASC) ,
  CONSTRAINT `fk_AlbumAttachments__album_id`
    FOREIGN KEY (`album_id` )
    REFERENCES `hunchWorks`.`Album` (`album_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_AlbumAttachments__attachment_id`
    FOREIGN KEY (`attachment_id` )
    REFERENCES `hunchWorks`.`Attachment` (`attachment_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`Class`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`Class` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`Class` (
  `class_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(45) NOT NULL ,
  `start_date` DATE NOT NULL ,
  `end_date` DATE NULL ,
  PRIMARY KEY (`class_id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hunchWorks`.`UserClass`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hunchWorks`.`UserClass` ;

CREATE  TABLE IF NOT EXISTS `hunchWorks`.`UserClass` (
  `user_class_id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `user_id` INT UNSIGNED NOT NULL ,
  `class_id` INT UNSIGNED NOT NULL ,
  PRIMARY KEY (`user_class_id`) ,
  INDEX `fk_UserClass_user_id` (`user_id` ASC) ,
  INDEX `fk_UserClass_class_id` (`class_id` ASC) ,
  CONSTRAINT `fk_UserClass_user_id`
    FOREIGN KEY (`user_id` )
    REFERENCES `hunchWorks`.`User` (`user_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_UserClass_class_id`
    FOREIGN KEY (`class_id` )
    REFERENCES `hunchWorks`.`Class` (`class_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
