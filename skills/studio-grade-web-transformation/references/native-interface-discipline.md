# Native and adaptive interface discipline (iOS / Android / webview)

Use for real native screens or hybrid products, not as compulsory procedure for a marketing website. Borrow platform-respecting *questions* from specialist native design practices, but rely on the CURRENT Apple Human Interface Guidelines, Android Material guidance, and actual app framework docs for implementation APIs.

1. **Identify platform contract:** native iOS, native Android, React Native, Flutter, webview or responsive web. Native navigation/back behavior, notification/permission consent and input semantics differ. A 390px browser screenshot is not an iOS simulator test.
2. **Make the primary task native:** use platform-appropriate tabs, gestures, scrolling, text input, dialogs, sheets, keyboard behavior and predictable back/resume semantics. Never turn a functional OS control into custom ornamental chrome without a real need.
3. **Dynamic content:** test larger text/font scaling, long names, translated copy, RTL where supported, rotation, display zoom, screen-reader labels, disabled/empty/loading/error states and touch exploration. Do not assume a single tap target size fits both OSes.
4. **System surfaces:** account for safe areas, notches, keyboard and software bars, reduced motion, high contrast, light/dark appearance, status/navigation bar visibility and foreground/background transitions.
5. **Motion and gestures:** preserve user control, spatial continuity and accessible alternatives; test both touch and assistive interactions.
6. **Evidence:** emulator/device and framework-specific checks, screen-reader passes (VoiceOver/TalkBack), screenshots for supported device classes and actual flow completion. If unavailable, mark them NOT TESTED rather than claiming native readiness.

For mobile-web only, use existing responsive/composition guides and actual browser testing instead. Avoid adding platform SDK assumptions or installing new dependencies without project authorization.
