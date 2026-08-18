# NovaStream Player

Cross-platform Flutter media-player foundation for Android, iOS, macOS and Windows.

## Deployment

The NovaStream work is isolated under `novastream/` so the existing Django application remains untouched. Codemagic configuration is in `novastream/codemagic.yaml`.

## Advertising policy

NovaStream ads are non-interruptive by design:

- Never pause or seek user media.
- Never cover the active video surface.
- Never inject audio during playback.
- Player ads live outside the media surface and are hidden while playback is active.
- Mobile uses test ad IDs in development; production IDs must be supplied through Codemagic secure environment variables.
- Desktop has no dependency on the mobile advertising SDK.
