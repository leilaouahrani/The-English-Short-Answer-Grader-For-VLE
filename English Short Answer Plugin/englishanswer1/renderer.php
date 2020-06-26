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


/**
 * Generates the output for arabicanswer1 questions.
 *
 *@copyright  2019 Snoussi El Hareth & Madani Abderraouf For C00L07UN100120180002 Project
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

//Question outputs
class qtype_arabicanswer1_renderer extends qtype_renderer {
    public function formulation_and_controls(question_attempt $qa,
            question_display_options $options) {

        $question = $qa->get_question();
        /**
     * Get the latest value of a particular question type variable. That is, get
     * the value from the latest step that has it set. Return null if it is not
     * set in any step.
     *
     * @param string $name the name of the variable to get.
     * @param mixed default the value to return in the variable has never been set.
     *      (Optional, defaults to null.)
     * @return mixed string value, or $default if it has never been set.
     */
        $currentanswer = $qa->get_last_qt_var('answer');
 /********************************************************************************************/

        /**
     * Get the name (in the sense a HTML name="" attribute, or a $_POST variable
     * name) to use for a question_type variable belonging to this question_attempt.
     *
     * See the comment on {@link question_attempt_step} for an explanation of
     * question type and behaviour variables.
     *
     * @param $varname The short form of the variable name.
     * @return string  The field name to use.
     */
        $inputname = $qa->get_qt_field_name('answer');
$inputattributes = array(
            'name' => $inputname,
            'id' => $inputname,
            'rows'=> 8,
            'cols'=>120,
            'class' => 'form-control d-inline',
        );
 /********************************************************************************************/

        /**question_display_options class qui contient l'attribut readonly
 * This class contains all the options that controls how a question is displayed.
 *
 * Normally, what will happen is that the calling code will set up some display
 * options to indicate what sort of question display it wants, and then before the
 * question is rendered, the behaviour will be given a chance to modify the
 * display options, so that, for example, A question that is finished will only
 * be shown read-only, and a question that has not been submitted will not have
 * any sort of feedback displayed.
 *
 */
        if ($options->readonly) {
            $inputattributes['readonly'] = 'readonly';
        }
        
/********************************************************************************************/

         $feedbackimg = '';
        
        
        /* correctness :(hidden / visible) whether the student gets told whether their answer was (in/partially)correct in the status summary under the question number, or instead are told something vague like 'Finished'.*/

        if ($options->correctness) {
            $fraction = $qa->get_fraction();
            $inputattributes['class'] .= ' ' . $this->feedback_class($fraction);
            /** feedback img:
     * Return an appropriate icon (green tick, red cross, etc.) for a grade.
     * @param float $fraction grade on a scale 0..1.
     * @param bool $selected whether to show a big or small icon. (Deprecated)
     * @return string html fragment.
     */
            $feedbackimg = $this->feedback_image($fraction);
        }
        
        /********************************************************************************************/
        
        /** @return the result of applying {@link format_text()} to the question text. */
        /*format_text()  * @return string the text formatted for output by format_text.*/
        $questiontext = $question->format_questiontext($qa);
        /********************************************************************************************/
        
        $placeholder = false;
        /*html_writer::empty_tag The final method empty_tag is used to create a self closing tag. This is useful in situations such as producing image tags, or input fields. It takes two arguments - tag and attributes, the same as start_tag.*/
       $input = html_writer::tag('textarea', $currentanswer,$inputattributes) . $feedbackimg;
        
 
        if (preg_match('/_____+/', $questiontext, $matches)) {
            $placeholder = $matches[0];
            $inputattributes['size'] = round(strlen($placeholder) * 1.1);
        }
        if ($placeholder) {
            /*html_writer::tag 
This method takes three arguments and is the combination of start_tag and end_tag plus the inclusion of content.

*/
           $inputinplace = html_writer::tag('label', get_string('answer'),
                    array('for' => $inputattributes['id'], 'class' => 'accesshide'));
            $inputinplace .= $input;
            $questiontext = substr_replace($questiontext, $inputinplace,
                    strpos($questiontext, $placeholder), strlen($placeholder));
        }

        $result = html_writer::tag('div', $questiontext, array('class' => 'qtext'));
        
        if (!$placeholder) {
            $result .= html_writer::start_tag('div', array('class' => 'ablock form-inline'));
            $result .= html_writer::tag('label', get_string('answer', 'qtype_arabicanswer1',
                    html_writer::tag('span', $input, array('class' => 'answer'))),
                    array('for' => $inputattributes['id']));
            $result .= html_writer::end_tag('div');
        }

         if ($qa->get_state() == question_state::$invalid) {
            $result .= html_writer::nonempty_tag('div',
                    $question->get_validation_error(array('answer' => $currentanswer)),
                    array('class' => 'validationerror'));
        }
        return $result;
    }

    // Feedback
    public function specific_feedback(question_attempt $qa) {
        $fraction = $qa->get_fraction();
        if(0.9 <=$fraction && $fraction <= 1){return get_string('verygood','qtype_arabicanswer1');  }
            else  if(0.75 <= $fraction && $fraction < 0.9){return get_string('good','qtype_arabicanswer1');  }
        else  if(0.6 <= $fraction && $fraction < 0.75){return get_string('satisfactory','qtype_arabicanswer1');  }
        else  if(0.5 <= $fraction && $fraction < 0.6){return get_string('average','qtype_arabicanswer1');  }
        else  if(0.25 <= $fraction && $fraction < 0.5){return get_string('poor','qtype_arabicanswer1');  }
                else {return get_string('failed','qtype_arabicanswer1');}
      
        
    }

    //Viewing the model response after an attempt
    public function correct_response(question_attempt $qa) {
        $question = $qa->get_question();
        $fraction = $qa->get_fraction();
        str_replace("\n", "", $qa->get_last_qt_var('answer'));

        $answer = $question->get_correct_response();
        if (!$answer) {
            return '';
        }
        
        if($fraction == 1)
        return get_string('modelansweris', 'qtype_arabicanswer1',
               $answer['answer']);

        if($fraction != 1)
        return get_string('correctansweris', 'qtype_arabicanswer1',
               $answer['answer']);
    }
    
}
