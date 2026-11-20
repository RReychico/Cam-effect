import unittest
from contextlib import ExitStack
from unittest.mock import Mock, patch

import numpy as np

from local_app import vanish_cam as app
from local_app.test_video_output import arguments


class ReverseReappearTests(unittest.TestCase):
    def run_reappear(self, mode, duration):
        clock = [0.0]
        background = np.full((24, 40, 3), 10, np.uint8)
        person = np.full((24, 40, 3), 200, np.uint8)
        # (time, frame, key pressed after this frame)
        r_at = 10.1
        script = [
            (0.0, background, 0), (2.0, background, 0), (4.1, background, 0),
            (4.2, person, ord("v")), (4.3, person, 0), (10.0, person, 0),
            (r_at, person, ord("r")), (r_at + duration / 2, person, 0),
            (r_at + duration + 0.1, person, 0), (r_at + duration + 0.2, person, ord("q")),
        ]
        capture = Mock()
        reads = iter(script)

        def read():
            t, frame, _ = next(reads)
            clock[0] = t
            return True, frame.copy()

        capture.read.side_effect = read
        segmenter, recognizer = Mock(), Mock()
        recognizer.recognize_joined_hands.return_value = False
        displayed = []
        with ExitStack() as mocks:
            mocks.enter_context(patch.object(app, "parse_args", return_value=arguments(mode=mode)))
            mocks.enter_context(patch.object(app, "download_models"))
            mocks.enter_context(patch.object(app, "open_camera", return_value=capture))
            mocks.enter_context(patch.object(app, "create_tasks", return_value=(segmenter, recognizer)))
            mocks.enter_context(patch.object(app, "open_virtual_camera", return_value=None))
            mocks.enter_context(patch.object(app, "VanishSound"))
            mask = np.zeros((24, 40), np.float32)
            mask[4:20, 10:30] = 1.0
            mocks.enter_context(patch.object(app, "person_mask", return_value=mask))
            mocks.enter_context(patch.object(app, "recognize_gesture", return_value=("No_Hand", 0.0)))
            mocks.enter_context(patch.object(app.time, "perf_counter", side_effect=lambda: clock[0]))
            mocks.enter_context(patch.object(app.cv2, "namedWindow"))
            mocks.enter_context(patch.object(app.cv2, "resizeWindow"))
            mocks.enter_context(patch.object(app.cv2, "destroyAllWindows"))
            mocks.enter_context(patch.object(app.cv2, "imshow", side_effect=lambda n, f: displayed.append(f.copy())))
            mocks.enter_context(patch.object(app.cv2, "waitKey", side_effect=[k for *_, k in script]))
            mocks.enter_context(patch("builtins.print"))
            self.assertEqual(app.run(), 0)
        return background, person, displayed

    def check(self, mode, duration):
        background, person, displayed = self.run_reappear(mode, duration)
        vanished, middle, done = displayed[6], displayed[7], displayed[8]
        if mode != "naruto":  # Naruto leaves the log on screen while vanished.
            np.testing.assert_array_equal(vanished, background)
        self.assertTrue(np.any(middle != background), "reverse effect should be drawing")
        self.assertTrue(np.any(middle != person), "person should not be fully back yet")
        np.testing.assert_array_equal(done, person)

    def test_normal_reverse_dissolve(self):
        self.check("normal", app.VANISH_SECONDS)

    def test_particles_reverse(self):
        self.check("particles", app.PARTICLE_SECONDS)

    def test_naruto_reverse(self):
        self.check("naruto", app.EFFECT_SECONDS)


if __name__ == "__main__":
    unittest.main()
