import cv2
import mediapipe as mp
import numpy as np
from fpdf import FPDF
import logging
from datetime import datetime
from typing import Dict, Optional

def draw_rounded_rect(img, rect_start, rect_end, corner_width, box_color):

    x1, y1 = rect_start
    x2, y2 = rect_end
    w = corner_width

    # draw filled rectangles
    cv2.rectangle(img, (x1 + w, y1), (x2 - w, y1 + w), box_color, -1)
    cv2.rectangle(img, (x1 + w, y2 - w), (x2 - w, y2), box_color, -1)
    cv2.rectangle(img, (x1, y1 + w), (x1 + w, y2 - w), box_color, -1)
    cv2.rectangle(img, (x2 - w, y1 + w), (x2, y2 - w), box_color, -1)
    cv2.rectangle(img, (x1 + w, y1 + w), (x2 - w, y2 - w), box_color, -1)


    # draw filled ellipses
    cv2.ellipse(img, (x1 + w, y1 + w), (w, w),
                angle = 0, startAngle = -90, endAngle = -180, color = box_color, thickness = -1)

    cv2.ellipse(img, (x2 - w, y1 + w), (w, w),
                angle = 0, startAngle = 0, endAngle = -90, color = box_color, thickness = -1)

    cv2.ellipse(img, (x1 + w, y2 - w), (w, w),
                angle = 0, startAngle = 90, endAngle = 180, color = box_color, thickness = -1)

    cv2.ellipse(img, (x2 - w, y2 - w), (w, w),
                angle = 0, startAngle = 0, endAngle = 90, color = box_color, thickness = -1)

    return img




def draw_dotted_line(frame, lm_coord, start, end, line_color):
    pix_step = 0

    for i in range(start, end+1, 8):
        cv2.circle(frame, (lm_coord[0], i+pix_step), 2, line_color, -1, lineType=cv2.LINE_AA)

    return frame


def draw_text(
    img,
    msg,
    width = 8,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    pos=(0, 0),
    font_scale=1,
    font_thickness=2,
    text_color=(0, 255, 0),
    text_color_bg=(0, 0, 0),
    box_offset=(20, 10),
):

    offset = box_offset
    x, y = pos
    text_size, _ = cv2.getTextSize(msg, font, font_scale, font_thickness)
    text_w, text_h = text_size
    rec_start = tuple(p - o for p, o in zip(pos, offset))
    rec_end = tuple(m + n - o for m, n, o in zip((x + text_w, y + text_h), offset, (25, 0)))
    
    img = draw_rounded_rect(img, rec_start, rec_end, width, text_color_bg)


    cv2.putText(
        img,
        msg,
        (int(rec_start[0] + 6), int(y + text_h + font_scale - 1)), 
        font,
        font_scale,
        text_color,
        font_thickness,
        cv2.LINE_AA,
    )

    
    return text_size




def find_angle(p1, p2, ref_pt = np.array([0,0])):
    p1_ref = p1 - ref_pt
    p2_ref = p2 - ref_pt

    cos_theta = (np.dot(p1_ref,p2_ref)) / (1.0 * np.linalg.norm(p1_ref) * np.linalg.norm(p2_ref))
    theta = np.arccos(np.clip(cos_theta, -1.0, 1.0))
            
    degree = int(180 / np.pi) * theta

    return int(degree)





def get_landmark_array(pose_landmark, key, frame_width, frame_height):

    denorm_x = int(pose_landmark[key].x * frame_width)
    denorm_y = int(pose_landmark[key].y * frame_height)

    return np.array([denorm_x, denorm_y])




def get_landmark_features(kp_results, dict_features, feature, frame_width, frame_height):

    if feature == 'nose':
        return get_landmark_array(kp_results, dict_features[feature], frame_width, frame_height)

    elif feature == 'left' or 'right':
        shldr_coord = get_landmark_array(kp_results, dict_features[feature]['shoulder'], frame_width, frame_height)
        elbow_coord   = get_landmark_array(kp_results, dict_features[feature]['elbow'], frame_width, frame_height)
        wrist_coord   = get_landmark_array(kp_results, dict_features[feature]['wrist'], frame_width, frame_height)
        hip_coord   = get_landmark_array(kp_results, dict_features[feature]['hip'], frame_width, frame_height)
        knee_coord   = get_landmark_array(kp_results, dict_features[feature]['knee'], frame_width, frame_height)
        ankle_coord   = get_landmark_array(kp_results, dict_features[feature]['ankle'], frame_width, frame_height)
        foot_coord   = get_landmark_array(kp_results, dict_features[feature]['foot'], frame_width, frame_height)

        return shldr_coord, elbow_coord, wrist_coord, hip_coord, knee_coord, ankle_coord, foot_coord
    
    else:
       raise ValueError("feature needs to be either 'nose', 'left' or 'right")


def get_mediapipe_pose(
                        static_image_mode = False, 
                        model_complexity = 1,
                        smooth_landmarks = True,
                        min_detection_confidence = 0.5,
                        min_tracking_confidence = 0.5

                      ):
    pose = mp.solutions.pose.Pose(
                                    static_image_mode = static_image_mode,
                                    model_complexity = model_complexity,
                                    smooth_landmarks = smooth_landmarks,
                                    min_detection_confidence = min_detection_confidence,
                                    min_tracking_confidence = min_tracking_confidence
                                 )
    return pose


class FitnessPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Title
        self.cell(0, 10, 'AI Fitness Trainer - Personalized Plan', 0, 1, 'C')
        # Line break
        self.ln(10)

def generate_pdf_report(plan: Dict) -> Optional[bytes]:
    try:
        pdf = FitnessPDF()
        pdf.add_page()

        # Add content sections
        add_summary_section(pdf, plan)
        add_macros_section(pdf, plan)
        add_workout_section(pdf, plan)
        add_hydration_section(pdf, plan)

        # Return PDF as bytes
        return pdf.output(dest='S').encode('latin-1')
    except Exception as e:
        logging.error(f"PDF generation failed: {str(e)}")
        return None

def add_summary_section(pdf: FitnessPDF, plan: Dict):
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Daily Summary", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Target Calories: {plan['daily_calories']} kcal", ln=True)
    pdf.ln(5)

def add_macros_section(pdf: FitnessPDF, plan: Dict):
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Macro Distribution", ln=True)
    pdf.set_font("Arial", "", 12)
    
    macros = plan.get('macros', {})
    if macros:
        pdf.cell(0, 8, f"Protein: {macros.get('protein', 0)}g", ln=True)
        pdf.cell(0, 8, f"Carbs: {macros.get('carbs', 0)}g", ln=True)
        pdf.cell(0, 8, f"Fats: {macros.get('fats', 0)}g", ln=True)
    pdf.ln(5)

def add_workout_section(pdf: FitnessPDF, plan: Dict):
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Weekly Workout Schedule", ln=True)
    
    schedule = plan.get('weekly_schedule', {})
    for day, workout in schedule.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"{day}: {workout['type'].title()}", ln=True)
        
        if workout['type'] != 'rest':
            pdf.set_font("Arial", "", 11)
            for exercise in workout.get('exercises', []):
                pdf.cell(10)  # indent
                pdf.multi_cell(0, 8, 
                    f"• {exercise['name']}\n  Sets: {exercise.get('sets', '-')}, "
                    f"Reps: {exercise.get('reps', exercise.get('duration', '-'))}")
        pdf.ln(3)

def add_hydration_section(pdf: FitnessPDF, plan: Dict):
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Hydration Guide", ln=True)
    pdf.set_font("Arial", "", 12)
    
    hydration = plan.get('hydration', {})
    if hydration:
        pdf.cell(0, 8, f"Daily Target: {hydration['daily_total_ml']/1000:.1f}L", ln=True)
        pdf.ln(3)
        for rec in hydration.get('recommendations', []):
            pdf.multi_cell(0, 8, f"• {rec}")