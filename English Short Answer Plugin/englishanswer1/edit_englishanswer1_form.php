<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Moodle is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Moodle.  If not, see <http://www.gnu.org/licenses/>.

/**
 * Defines the editing form for the arabicanswer question type.
 *
 * @package    qtype
 * @subpackage arabicanswer1
 * @copyright  2019 Snoussi El Hareth & Madani Abderraouf For C00L07UN100120180002 Project
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */


defined('MOODLE_INTERNAL') || die();

/*question form for our short answer grader */
/**
 *arabicanswer1 question editing form definition.
 *
 * @copyright  2019 Snoussi El Hareth & Madani Abderraouf For C00L07UN100120180002 Project

 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */
class qtype_arabicanswer1_edit_form extends question_edit_form {

    //Add question form
   protected function definition_inner($mform) {
       global $CFG ;
       
    
        $mform->addElement('static', 'answersinstruct',
                get_string('modelanswer', 'qtype_arabicanswer1'),
                get_string('provideanswer', 'qtype_arabicanswer1'));
        $mform->closeHeaderBefore('answersinstruct');

       
       $mform->addElement('header', 'answerhdr',
                    get_string('answers', 'question'), '');
        $mform->setExpanded('answerhdr', 1);

        $answersoption = '';
        $repeatedoptions = array();
      
       
       // $mform->addElement('text', 'answer', get_string('modelanswer', 'qtype_arabicanswer1'),
                //array('size' => 150, 'maxlength' => 500));
       $mform->addElement('textarea', 'answer',  get_string('modelanswer', 'qtype_arabicanswer1'), 'wrap="virtual" rows="10" cols="120"');
       $mform->setType('answer', PARAM_TEXT);
       $mform->addRule('answer', null, 'required', null, 'client');
      
 
        
    }
    
    /*
     * Perform an preprocessing needed on the data passed to {@link set_data()}
     * before it is used to initialise the form.
     * @param object $question the data being passed to the form.
     * @return object $question the modified data.
     */
    protected function data_preprocessing($question) {
     $question = parent::data_preprocessing($question);
      if (empty($question->options->answers)) {
            return $question;
        }
        
         /**
     * Perform the necessary preprocessing for the fields added by
     * {@link add_per_answer_fields()}.
     * @param object $question the data being passed to the form.
     * @return object $question the modified data.
     */
        foreach ($question->options->answers as $answer){
        $question->answer = $answer->answer;
               }
                
        return $question;
    }


    public function qtype() {
        return 'arabicanswer1';
    }
}
