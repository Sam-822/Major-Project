
-- --------------------------------------------------------

--
-- Table structure for table `student_details`
--

DROP TABLE IF EXISTS `student_details`;
CREATE TABLE IF NOT EXISTS `student_details` (
  `moodle_id` varchar(8) NOT NULL,
  `name` varchar(40) NOT NULL,
  `year` varchar(4) NOT NULL,
  `department` varchar(30) NOT NULL,
  `password` varchar(64) NOT NULL,
  `moodle_email_id` varchar(25) NOT NULL,
  PRIMARY KEY (`moodle_id`),
  UNIQUE KEY `moodle_email_id` (`moodle_email_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student_details`
--

INSERT INTO `student_details` (`moodle_id`, `name`, `year`, `department`, `password`, `moodle_email_id`) VALUES
('19104037', 'AbhayPratap Singh', 'B.E.', 'Information Technology', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', '19104037@apsit.edu.in');
