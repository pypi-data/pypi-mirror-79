import cv2
from typing import List, Tuple, Callable, Optional
import numpy as np

from src.types import Frame
from src.constants import \
    PT_PIXEL_BYTES_FORMAT, \
    IR_ROUND_PIXEL, \
    BUFFER_FRAME_SEPARATOR


def get_frames_configuration(
        pt_frames: [Frame]
) -> Tuple[Optional[List], Optional[int], Optional[Callable], Optional[Callable]]:
    size, mice_count, group_frames, concatenate_groups = None, None, None, None
    if len(pt_frames) == 3:
        size = [320, 160]
        mice_count = 1

        def group_frames(pt_frames: [Frame]) -> List[List[Frame]]:
            return [[
                cv2.rotate(pt_frames[0][:-20], cv2.ROTATE_90_COUNTERCLOCKWISE),
                cv2.rotate(pt_frames[2][:-20], cv2.ROTATE_90_COUNTERCLOCKWISE),
                cv2.rotate(pt_frames[1], cv2.ROTATE_90_COUNTERCLOCKWISE),
            ]]

        def concatenate_groups(frame_groups: List[List[Frame]]) -> List[Frame]:
            return [np.concatenate(frame_groups[0], axis=1)]

    if len(pt_frames) == 4:
        size = [300, 240]
        mice_count = 2

        def group_frames(pt_frames: [Frame]) -> List[List[Frame]]:
            return [
                [pt_frames[0][:, :-20], pt_frames[3]],
                [pt_frames[1][:, :-20], pt_frames[2]],
            ]

        def concatenate_groups(frame_groups: List[List[Frame]]) -> List[Frame]:
            return [
                np.concatenate(frame_groups[0], axis=1),
                np.concatenate(frame_groups[1], axis=1),
            ]

    return size, mice_count, group_frames, concatenate_groups


def normalize_frame(frame: Frame) -> Frame:
    cv2.normalize(frame, frame, 0, 65535, cv2.NORM_MINMAX)
    np.right_shift(frame, 8, frame)

    return frame


def clear_pt_frame(frame):
    return frame[:-2]


def process_pt_frame(frame: Frame) -> Frame:
    return normalize_frame(
        clear_pt_frame(frame),
    )


def process_ir_frame(frame: Frame) -> Frame:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.normalize(frame, frame, 0, IR_ROUND_PIXEL, cv2.NORM_MINMAX)

    return frame


def get_temperatures(groups: List[List[Frame]]) -> List[List[int]]:
    return [
        [min([np.min(frame) for frame in group]), max([np.max(frame) for frame in group])]
        for group in groups
    ]


def resize_frame(frame: Frame, size: [int]) -> Frame:
    return cv2.resize(frame, tuple(size), interpolation=cv2.INTER_AREA)


def put_text(frame: Frame, coordinates: [int], text: str):
    cv2.putText(
        frame,
        text=text,
        org=tuple(coordinates),
        fontFace=cv2.FONT_ITALIC,
        fontScale=0.3,
        thickness=1,
        color=190,
    )


def show_frame(frame: Frame, index=''):
    cv2.imshow(f'streaming {index}', frame / np.max(frame))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise KeyboardInterrupt('stopping stream')


def int16_to_bytes(value: int, length: int = 2) -> bytes:
    return value.to_bytes(length, PT_PIXEL_BYTES_FORMAT)


def make_frame_buffer(temperatures: [[int]], frames: [Frame]) -> bytes:
    return BUFFER_FRAME_SEPARATOR.join(
        b''.join(map(int16_to_bytes, map(int, temperatures[index]))) + frame.astype(np.uint8).flatten().tostring()
        for index, frame in enumerate(frames)
    )
