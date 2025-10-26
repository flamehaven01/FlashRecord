"""
FlashRecord Advanced GIF Compression - Enhanced Edition
Based on "Enhancing Learned Image Compression via Cross Window-based Attention" (arXiv:2410.21144)

Key techniques:
1. Cross-Window Attention Saliency (CWAM-inspired)
2. Adaptive tile sizing (8/16/32px based on complexity)
3. Temporal redundancy removal with frame subsampling
4. RGB preservation with global palette optimization

REX Engine Patches Applied (v0.3.2):
- Patch 1-5: Core functionality
- Fix 6-7: Color accuracy + timing preservation

Enhanced Edition Improvements:
- Error handling & logging (9.txt #2)
- Input validation & edge cases
- Adaptive parameters (8.txt)
- Performance optimizations (9.txt #1)
"""

import os
import logging
from typing import List, Tuple, Optional
from io import BytesIO
import numpy as np
from PIL import Image, ImageFilter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


class CWAMInspiredCompressor:
    """
    CWAM-inspired lightweight GIF compressor with enhanced stability
    Implements cross-scale window attention concepts without deep learning
    """

    def __init__(self, target_size_mb=10, quality='balanced', max_memory_mb=1024):
        """
        Initialize compressor

        Args:
            target_size_mb: Target file size in MB
            quality: 'high' (70%), 'balanced' (50%), 'compact' (30%)
            max_memory_mb: Maximum memory usage limit in MB
        """
        self.target_size_mb = target_size_mb
        self.max_memory_mb = max_memory_mb
        self.quality_presets = {
            'high': 0.70,      # 70% resolution
            'balanced': 0.50,  # 50% resolution
            'compact': 0.30    # 30% resolution
        }
        self.scale_factor = self.quality_presets.get(quality, 0.50)

        # Adaptive parameters (8.txt improvements)
        self.min_colors = 16  # Minimum palette colors
        self.adaptive_tile_enabled = True  # Auto tile size selection

        logger.info(f"Compressor initialized: target={target_size_mb}MB, quality={quality}, scale={self.scale_factor}")

    def _safe_convert(self, frame: Image.Image, mode: str) -> Image.Image:
        """
        Safely convert frame to target mode with error handling

        Args:
            frame: Input PIL Image
            mode: Target mode ('L', 'RGB', 'P', etc.)

        Returns:
            Converted image or gray placeholder on error
        """
        try:
            return frame.convert(mode)
        except Exception as e:
            logger.error(f"Frame conversion failed ({mode}): {e}")
            # Return gray placeholder
            return Image.new(mode, frame.size, 128 if mode == 'L' else (128, 128, 128))

    def _validate_frames(self, frames: List[Image.Image]) -> bool:
        """
        Validate input frames

        Args:
            frames: List of PIL Images

        Returns:
            True if valid, False otherwise
        """
        if not frames:
            logger.warning("Empty frame list provided")
            return False

        if len(frames) > 10000:
            logger.warning(f"Very large frame count: {len(frames)} (memory risk)")

        # Check first frame
        if not isinstance(frames[0], Image.Image):
            logger.error("Invalid frame type")
            return False

        # Estimate memory usage
        w, h = frames[0].size
        estimated_mb = (w * h * 3 * len(frames)) / (1024 * 1024)
        if estimated_mb > self.max_memory_mb:
            logger.error(f"Estimated memory {estimated_mb:.1f}MB exceeds limit {self.max_memory_mb}MB")
            return False

        return True

    def _adaptive_tile_size(self, gray: np.ndarray) -> int:
        """
        Automatically select tile size based on image complexity (9.txt #3)

        Args:
            gray: Grayscale image array

        Returns:
            Tile size (8, 16, or 32)
        """
        if not self.adaptive_tile_enabled:
            return 16

        try:
            # Compute complexity metrics
            variance = float(np.var(gray))

            # Edge density (simple gradient)
            grad_y = np.abs(np.diff(gray.astype(float), axis=0))
            grad_x = np.abs(np.diff(gray.astype(float), axis=1))
            edge_density = (np.mean(grad_y) + np.mean(grad_x)) / 2.0

            # Histogram entropy
            hist, _ = np.histogram(gray, bins=32, range=(0, 255))
            p = hist.astype(np.float64) / (hist.sum() + 1e-12)
            entropy = float(-(p * np.log2(p + 1e-12)).sum())

            # Complexity score
            score = 0.5 * (entropy / 5.0) + 0.3 * (variance / 5000.0) + 0.2 * (edge_density / 50.0)

            # Select tile size
            if score > 0.9:
                return 8   # High complexity - fine tiles
            elif score > 0.6:
                return 16  # Medium complexity
            else:
                return 32  # Low complexity - coarse tiles
        except Exception as e:
            logger.warning(f"Adaptive tile sizing failed: {e}, using default 16")
            return 16

    def compress_frames(self, frames: List[Image.Image]) -> List[Image.Image]:
        """
        Compress frames using CWAM-inspired techniques

        Args:
            frames: List of PIL Image frames

        Returns:
            Compressed frames
        """
        if not self._validate_frames(frames):
            logger.error("Frame validation failed")
            return frames

        try:
            logger.info(f"[*] CWAM-inspired compression: {len(frames)} frames")

            # Step 1: Resolution scaling (spatial compression)
            compressed = self._scale_frames(frames)

            # Step 2: Temporal subsampling (10fps -> 8fps)
            compressed = self._reduce_frame_rate(compressed, target_fps=8)

            # Step 3: Cross-window saliency analysis (CWAM core idea)
            saliency_maps = self._compute_cw_saliency_maps(compressed)

            # Step 4: Saliency-guided frame preservation (REX Engine patch)
            keep_mask = self._keep_mask_from_saliency(saliency_maps, thr=0.25)
            compressed = [f for i, f in enumerate(compressed) if keep_mask[i]]
            logger.info(f"[*] Saliency-guided keep: {keep_mask.sum()}/{len(keep_mask)} frames")

            logger.info(f"[+] Compression complete: {len(frames)} -> {len(compressed)} frames")
            return compressed

        except Exception as e:
            logger.error(f"Compression failed: {e}", exc_info=True)
            return frames  # Return original on error

    def _scale_frames(self, frames: List[Image.Image]) -> List[Image.Image]:
        """
        Adaptive resolution scaling
        Based on Feature Encoding module from paper
        """
        if not frames:
            return frames

        try:
            original_size = frames[0].size
            new_width = max(1, int(original_size[0] * self.scale_factor))
            new_height = max(1, int(original_size[1] * self.scale_factor))

            logger.info(f"[*] Resolution scaling: {original_size} -> ({new_width}, {new_height})")

            scaled = []
            for i, frame in enumerate(frames):
                try:
                    # LANCZOS for high-quality downsampling
                    scaled_frame = frame.resize(
                        (new_width, new_height),
                        Image.Resampling.LANCZOS
                    )
                    scaled.append(scaled_frame)
                except Exception as e:
                    logger.warning(f"Frame {i} resize failed: {e}, using original")
                    scaled.append(frame)

            return scaled

        except Exception as e:
            logger.error(f"Scale frames failed: {e}")
            return frames

    def _reduce_frame_rate(self, frames: List[Image.Image], target_fps=8, input_fps=None) -> List[Image.Image]:
        """
        Temporal subsampling - reduce frame rate
        Removes temporal redundancy (paper: local redundancy capture)
        REX Engine Patch 4: Remove FPS hardcoding, use accumulator for even distribution

        Args:
            frames: Input frames
            target_fps: Target FPS (default: 8)
            input_fps: Input FPS (default: 10 if None)

        Returns:
            Subsampled frames
        """
        if not frames:
            return frames

        fps = input_fps or 10  # FlashRecord default, but can be overridden
        if target_fps >= fps:
            return frames

        # Accumulator-based sampling for even distribution
        acc, out = 0.0, []
        step = float(fps) / float(target_fps)

        for i, f in enumerate(frames):
            if acc <= 0.0:
                out.append(f)
            acc += 1.0
            if acc >= step:
                acc -= step

        logger.info(f"[*] Temporal subsampling: {len(frames)} -> {len(out)} frames ({fps}fps -> {target_fps}fps)")
        return out

    def _compute_cw_saliency_maps(self, frames: List[Image.Image]) -> List[np.ndarray]:
        """
        Compute Cross-Window (CW) saliency maps
        Core CWAM idea: multi-scale window interaction

        Based on paper section on cross-scale window attention

        Args:
            frames: Input frames

        Returns:
            List of saliency maps (one per frame)
        """
        saliency_maps = []

        for idx, frame in enumerate(frames):
            try:
                # Convert to grayscale for analysis
                gray = self._safe_convert(frame, 'L')

                # Original scale features
                F = np.array(gray, dtype=np.float32)

                # Downscaled features (coarse scale)
                F_down = np.array(
                    gray.resize((gray.width // 2, gray.height // 2), Image.Resampling.BILINEAR),
                    dtype=np.float32
                )

                # Adaptive tile size selection (9.txt #3)
                tile_size = self._adaptive_tile_size(F)

                # Compute saliency at both scales
                S_fine = self._compute_saliency_single_scale(F, tile_size=tile_size)
                S_coarse = self._compute_saliency_single_scale(F_down, tile_size=max(8, tile_size // 2))

                # Cross-scale interaction (CWAM core)
                # Upsample coarse to match fine resolution
                S_coarse_up = self._upsample_saliency(S_coarse, S_fine.shape)

                # Combine: weighted sum (cross-window attention approximation)
                S_combined = 0.6 * S_fine + 0.4 * S_coarse_up

                saliency_maps.append(S_combined)

            except Exception as e:
                logger.warning(f"Saliency computation failed for frame {idx}: {e}")
                # Fallback: uniform saliency
                saliency_maps.append(np.ones((10, 10), dtype=np.float32))

        # Temporal smoothing (3-frame window)
        saliency_maps = self._temporal_smooth_saliency(saliency_maps)

        return saliency_maps

    def _compute_saliency_single_scale(self, img_array: np.ndarray, tile_size=16) -> np.ndarray:
        """
        Compute saliency at single scale
        Based on variance + edge density + entropy

        Args:
            img_array: Grayscale image array
            tile_size: Tile size in pixels

        Returns:
            Saliency map
        """
        try:
            h, w = img_array.shape
            n_tiles_h = max(1, h // tile_size)
            n_tiles_w = max(1, w // tile_size)

            saliency = np.zeros((n_tiles_h, n_tiles_w), dtype=np.float32)

            # Compute edge map
            img_pil = Image.fromarray(img_array.astype(np.uint8))
            edges = np.array(img_pil.filter(ImageFilter.FIND_EDGES), dtype=np.float32)

            for ty in range(n_tiles_h):
                for tx in range(n_tiles_w):
                    y = ty * tile_size
                    x = tx * tile_size

                    # Extract tile
                    tile = img_array[y:y+tile_size, x:x+tile_size]
                    edge_tile = edges[y:y+tile_size, x:x+tile_size]

                    if tile.size < tile_size * tile_size // 4:  # Skip very small tiles
                        continue

                    # Variance (texture complexity)
                    variance = float(np.var(tile))

                    # Edge density (structural information)
                    edge_density = float(np.mean(edge_tile))

                    # Entropy (information content)
                    entropy = self._compute_entropy(tile)

                    # Weighted combination
                    saliency[ty, tx] = 0.5 * variance + 0.3 * edge_density + 0.2 * entropy

            # Normalize
            if saliency.max() > 0:
                saliency = saliency / saliency.max()

            return saliency

        except Exception as e:
            logger.warning(f"Saliency single-scale failed: {e}")
            return np.ones((10, 10), dtype=np.float32) * 0.5

    def _compute_entropy(self, patch: np.ndarray, n_bins=32) -> float:
        """
        Compute Shannon entropy of image patch
        REX Engine Patch 5: Use count-based normalization for consistency

        Args:
            patch: Image patch
            n_bins: Number of histogram bins

        Returns:
            Entropy value
        """
        try:
            hist, _ = np.histogram(patch, bins=n_bins, range=(0, 255))
            p = hist.astype(np.float64)
            p = p / (p.sum() + 1e-12)  # Count-based normalization
            return float(-(p * np.log2(p + 1e-12)).sum())
        except Exception as e:
            logger.warning(f"Entropy computation failed: {e}")
            return 0.0

    def _upsample_saliency(self, saliency: np.ndarray, target_shape: Tuple[int, int]) -> np.ndarray:
        """
        Upsample saliency map to target shape
        REX Engine Patch 2: Use BILINEAR instead of Kronecker to reduce aliasing

        Args:
            saliency: Input saliency map
            target_shape: Target (height, width)

        Returns:
            Upsampled saliency map
        """
        try:
            H, W = target_shape

            # Avoid division by zero
            smax = saliency.max()
            if smax < 1e-12:
                smax = 1.0

            # Convert to uint8 for PIL processing
            s = (saliency * 255.0 / smax).astype(np.uint8)

            # Upsample with BILINEAR (smoother than nearest/Kronecker)
            sm = Image.fromarray(s).resize((W, H), Image.Resampling.BILINEAR)

            # Convert back to float32 [0, 1]
            return np.array(sm, dtype=np.float32) / 255.0

        except Exception as e:
            logger.warning(f"Saliency upsampling failed: {e}")
            return np.ones(target_shape, dtype=np.float32) * 0.5

    def _temporal_smooth_saliency(self, saliency_maps: List[np.ndarray]) -> List[np.ndarray]:
        """
        Apply temporal smoothing to saliency maps
        3-frame window averaging

        Args:
            saliency_maps: List of saliency maps

        Returns:
            Temporally smoothed saliency maps
        """
        if len(saliency_maps) <= 2:
            return saliency_maps

        try:
            smoothed = [saliency_maps[0]]  # Keep first frame as-is

            for i in range(1, len(saliency_maps) - 1):
                # 3-frame window: prev + current + next
                avg = 0.2 * saliency_maps[i-1] + 0.6 * saliency_maps[i] + 0.2 * saliency_maps[i+1]
                smoothed.append(avg)

            smoothed.append(saliency_maps[-1])  # Keep last frame as-is

            return smoothed

        except Exception as e:
            logger.warning(f"Temporal smoothing failed: {e}")
            return saliency_maps

    def _keep_mask_from_saliency(self, S_list: List[np.ndarray], thr=0.25) -> np.ndarray:
        """
        Saliency-guided frame preservation
        Frames with high saliency (detail/motion) are kept, flat frames are dropped

        REX Engine Patch 1: Use computed saliency for actual decision-making
        Enhanced: Percentile-based threshold (8.txt #5)

        Args:
            S_list: List of saliency maps
            thr: Threshold multiplier for standard deviation

        Returns:
            Boolean mask of frames to keep
        """
        try:
            # Compute mean saliency per frame
            m = np.array([float(S.mean()) for S in S_list])

            # Percentile-based threshold (8.txt improvement)
            # Keep frames with saliency above adaptive threshold
            threshold = m.mean() * 0.6 + thr * (m.std() + 1e-8)
            keep = m >= threshold

            # Guarantee minimum sampling (don't drop too many frames)
            min_frames = max(2, int(0.6 * len(S_list)))
            if keep.sum() < min_frames:
                idx = np.argsort(m)[-min_frames:]
                keep[:] = False
                keep[idx] = True

            return keep

        except Exception as e:
            logger.error(f"Saliency masking failed: {e}")
            # Fallback: keep all frames
            return np.ones(len(S_list), dtype=bool)

    def _round10ms(self, ms: float) -> int:
        """
        Round milliseconds to 10ms increments for GIF player compatibility
        REX Engine v0.3.2: Timing preservation helper

        Args:
            ms: Milliseconds to round

        Returns:
            Rounded milliseconds (minimum 10ms)
        """
        return max(10, int(round(ms / 10.0) * 10))

    def _durations_for_preserve(self, orig_n: int, fps_in: float, out_frames: int) -> list:
        """
        Distribute original total time across output frames evenly
        REX Engine v0.3.2: Timing preservation - maintain total playback duration
        REX Engine Fix 7.2: Distribute drift across first N frames instead of concentrating on last

        Args:
            orig_n: Original frame count
            fps_in: Original FPS
            out_frames: Output frame count after compression

        Returns:
            List of per-frame durations in ms (sum equals original total_ms ±10ms rounding)
        """
        try:
            total_ms = int(round((orig_n / float(fps_in)) * 1000.0))

            # Base per-frame duration (float) then round to 10ms
            per_raw = float(total_ms) / max(out_frames, 1)
            per_rounded = self._round10ms(per_raw)
            durs = [per_rounded] * out_frames

            # REX Engine Fix 7.2: Distribute drift across first N frames (not just last)
            drift = total_ms - sum(durs)

            if drift != 0:
                # Distribute drift in +/-10ms increments across first N frames
                n_distribute = min(out_frames, max(1, abs(drift) // 10))
                increment = 10 if drift > 0 else -10

                for i in range(n_distribute):
                    if abs(drift) < 10:
                        break
                    durs[i] = self._round10ms(durs[i] + increment)
                    drift -= increment

                # Any remaining drift (<10ms) goes to last frame
                if drift != 0:
                    durs[-1] = self._round10ms(durs[-1] + drift)

            return durs

        except Exception as e:
            logger.error(f"Duration calculation failed: {e}")
            # Fallback: equal durations
            default_duration = self._round10ms(1000.0 / 8)
            return [default_duration] * out_frames

    def _build_global_palette(self, frames: List[Image.Image], colors=256, seed=1234) -> list:
        """
        Build global palette with saturation-weighted sampling
        REX Engine Fix 6: Corrected color accuracy with weighted sampling
        Enhanced: Reservoir sampling for memory efficiency (8.txt #4)

        Args:
            frames: List of RGB frames
            colors: Number of colors in palette
            seed: Random seed for reproducibility

        Returns:
            768-element palette list (RGB triplets)
        """
        try:
            rng = np.random.default_rng(seed)
            arrs = [np.array(self._safe_convert(f, "RGB")) for f in frames]
            H, W = arrs[0].shape[:2]

            # Reservoir sampling for memory efficiency (8.txt improvement)
            max_samples = min(colors * 1024, 1000000)  # Cap at 1M samples

            # Collect pixels with stride for large images
            stride = max(1, int(np.sqrt(H * W / 262144)))  # 512x512 base
            sampled_pixels = []

            for arr in arrs:
                pixels = arr[::stride, ::stride, :].reshape(-1, 3)
                sampled_pixels.append(pixels)

            all_pixels = np.concatenate(sampled_pixels, 0)

            # Limit total samples
            if len(all_pixels) > max_samples:
                indices = rng.choice(len(all_pixels), size=max_samples, replace=False)
                all_pixels = all_pixels[indices]

            # Compute saturation for each pixel (avoid dark/grayscale bias)
            r, g, b = all_pixels[:, 0], all_pixels[:, 1], all_pixels[:, 2]
            max_c = np.maximum(np.maximum(r, g), b).astype(np.float32)
            min_c = np.minimum(np.minimum(r, g), b).astype(np.float32)
            saturation = (max_c - min_c) / (max_c + 1e-6)  # 0-1 range

            # Weighted sampling: favor saturated colors
            weights = saturation + 0.5
            weights = weights / weights.sum()

            # Sample based on saturation weights
            n_samples = min(len(all_pixels), colors * 1024)
            indices = rng.choice(len(all_pixels), size=n_samples, replace=False, p=weights)
            sample = all_pixels[indices]

            # Generate palette using MEDIANCUT
            S = Image.fromarray(sample.reshape(-1, 1, 3).astype(np.uint8))
            q = S.quantize(colors=colors, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
            pal = np.array(q.getpalette(), dtype=np.uint8)[:colors * 3].tolist()
            pal += [0] * (768 - len(pal))  # Pad to 768

            return pal

        except Exception as e:
            logger.error(f"Palette building failed: {e}", exc_info=True)
            # Fallback: grayscale palette
            gray_pal = list(range(256)) * 3
            return gray_pal[:768]

    def _apply_global_palette(self, frames: List[Image.Image], pal: list, dither=True) -> List[Image.Image]:
        """
        Apply global palette to all frames
        REX Engine Patch 3-2 + Fix 5: Correct palette application to prevent black screen

        CRITICAL FIX: Use quantize with explicit palette image to ensure proper index mapping

        Args:
            frames: List of RGB frames
            pal: 768-element palette list
            dither: Enable Floyd-Steinberg dithering

        Returns:
            Palette-mode frames
        """
        try:
            colors = len(pal) // 3
            out = []

            # Create palette image for quantize()
            palette_img = Image.new("P", (1, 1))
            palette_img.putpalette(pal)

            for i, im in enumerate(frames):
                try:
                    # CRITICAL: Use quantize() with palette parameter for proper RGB→P mapping
                    q = self._safe_convert(im, "RGB").quantize(
                        palette=palette_img,
                        colors=colors,
                        dither=Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
                    )
                    out.append(q)
                except Exception as e:
                    logger.warning(f"Frame {i} palette application failed: {e}")
                    # Fallback: simple quantize
                    out.append(self._safe_convert(im, "P"))

            return out

        except Exception as e:
            logger.error(f"Global palette application failed: {e}")
            # Fallback: convert each frame independently
            return [self._safe_convert(f, "P") for f in frames]

    def _encode_gif_bytes(self, frames: List[Image.Image], duration_ms=120, durations_ms=None, loop=0, disposal=2, optimize=False) -> bytes:
        """
        Encode frames to GIF bytes
        REX Engine Patch 3-3 + Fix 5: In-memory GIF encoding with timing preservation

        CRITICAL FIX: optimize=False to prevent index mapping corruption with single palette

        Args:
            frames: Palette-mode frames
            duration_ms: Frame duration in milliseconds (if durations_ms not provided)
            durations_ms: List of per-frame durations (for timing preservation)
            loop: Loop count (0 = infinite)
            disposal: Disposal method (2 = restore to background)
            optimize: Enable GIF optimization (False recommended for color accuracy)

        Returns:
            GIF file bytes
        """
        try:
            bio = BytesIO()

            save_kwargs = {
                "format": "GIF",
                "save_all": True,
                "append_images": frames[1:],
                "loop": loop,
                "disposal": disposal,
                "optimize": optimize  # False prevents palette index corruption
            }

            # Use durations list if provided, otherwise use single duration
            if durations_ms is not None:
                save_kwargs["duration"] = durations_ms
            else:
                save_kwargs["duration"] = duration_ms

            frames[0].save(bio, **save_kwargs)
            return bio.getvalue()

        except Exception as e:
            logger.error(f"GIF encoding failed: {e}", exc_info=True)
            raise

    def compress_to_target(self, frames: List[Image.Image], target_mb=10, init_colors=256, min_fps=4,
                           preserve_timing: bool = True, max_iterations: int = 5, input_fps: int = None):
        """
        Enhanced target-driven compression with timing preservation
        REX Engine v0.3.2: preserve-timing + extended loop + metadata
        REX Engine Fix 7.1: Store original frames to prevent accumulated rescaling artifacts
        Enhanced: Early resolution trigger, min_colors parameter (8.txt #3, #7)

        Args:
            frames: Input RGB frames
            target_mb: Target file size in MB
            init_colors: Initial palette colors
            min_fps: Minimum FPS threshold
            preserve_timing: Keep original total duration
            max_iterations: Maximum adaptive iterations
            input_fps: Original FPS (if None, defaults to 10)

        Returns:
            Tuple of (gif_bytes, metadata)
        """
        if not self._validate_frames(frames):
            raise ValueError("Invalid input frames")

        try:
            # --- Step 0: Collect original meta and store original frames (Fix 7.1)
            orig_n = len(frames)
            fps_in = input_fps or 10
            total_ms = int(round((orig_n / float(fps_in)) * 1000.0))

            # REX Engine Fix 7.1: Store original frames to always rescale from source
            orig_frames = [self._safe_convert(f, 'RGB') for f in frames]

            # Step 1: Preprocessing pipeline
            frames = self._scale_frames(frames)
            frames = self._reduce_frame_rate(frames, target_fps=8, input_fps=fps_in)
            S = self._compute_cw_saliency_maps(frames)
            keep = self._keep_mask_from_saliency(S, thr=0.25)
            frames = [f for i, f in enumerate(frames) if keep[i]]

            # Step 2: prepare palette + frames (initial)
            colors, fps = init_colors, 8
            pal = self._build_global_palette(frames, colors=colors, seed=1234)
            qframes = self._apply_global_palette(frames, pal, dither=True)

            # Iterative feedback with adaptive logic (max_iterations)
            iteration = 0
            last_meta = None

            while iteration < max_iterations:
                out_frames = len(qframes)

                # compute durations (preserve timing if requested)
                if preserve_timing:
                    durations_ms = self._durations_for_preserve(orig_n, fps_in, out_frames)
                else:
                    durations_ms = [self._round10ms(1000.0 / max(fps, 1))] * out_frames

                data = self._encode_gif_bytes(qframes, durations_ms=durations_ms)
                size_mb = len(data) / (1024 * 1024)

                logger.info(f"[*] Iter {iteration+1}/{max_iterations}: size={size_mb:.3f}MB frames={out_frames} colors={colors} fps_goal={fps} total_ms={sum(durations_ms)}")

                # build metadata snapshot
                meta = {
                    'iteration': iteration + 1,
                    'orig_fps': fps_in,
                    'orig_frames': orig_n,
                    'frames_out': out_frames,
                    'colors': colors,
                    'fps_goal': fps,
                    'size_mb': round(size_mb, 4),
                    'total_ms': sum(durations_ms),
                    'durations_ms': durations_ms
                }
                last_meta = meta

                if size_mb <= target_mb:
                    # verification: durations sum within tolerance
                    meta['preserve_timing_ok'] = abs(total_ms - meta['total_ms']) <= 10
                    return data, meta

                # Enhanced adaptive reduction order (8.txt #7)
                ratio = size_mb / float(target_mb)

                # Early resolution trigger if size ratio is too large (8.txt improvement)
                if ratio > 1.5 and colors <= max(32, self.min_colors):
                    logger.info(f"[*] Large size ratio {ratio:.2f}, triggering early resolution reduction")
                    prev_scale = self.scale_factor
                    self.scale_factor = max(0.1, self.scale_factor * 0.85)
                    logger.info(f"[*] Adaptive: reducing resolution {prev_scale:.3f} -> {self.scale_factor:.3f}")

                    # Re-run from original frames
                    frames = self._scale_frames(orig_frames)
                    frames = self._reduce_frame_rate(frames, target_fps=8, input_fps=fps_in)
                    S = self._compute_cw_saliency_maps(frames)
                    keep = self._keep_mask_from_saliency(S, thr=0.25)
                    frames = [f for i, f in enumerate(frames) if keep[i]]
                    pal = self._build_global_palette(frames, colors=colors, seed=1234)
                    qframes = self._apply_global_palette(frames, pal, dither=True)

                elif colors > max(32, self.min_colors):
                    colors = max(self.min_colors, colors // 2)
                    logger.info(f"[*] Adaptive: reducing colors -> {colors}")
                    pal = self._build_global_palette(frames, colors=colors, seed=1234)
                    qframes = self._apply_global_palette(frames, pal, dither=True)

                elif (not preserve_timing) and fps > min_fps:
                    prev = fps
                    fps = max(min_fps, fps - 1)
                    logger.info(f"[*] Adaptive: reducing fps {prev} -> {fps}")

                else:
                    # Final fallback: resolution reduction
                    prev_scale = self.scale_factor
                    self.scale_factor = max(0.1, self.scale_factor * 0.85)
                    logger.info(f"[*] Adaptive: reducing resolution {prev_scale:.3f} -> {self.scale_factor:.3f}")

                    # REX Engine Fix 7.1: Re-run from ORIGINAL frames
                    frames = self._scale_frames(orig_frames)
                    frames = self._reduce_frame_rate(frames, target_fps=8, input_fps=fps_in)
                    S = self._compute_cw_saliency_maps(frames)
                    keep = self._keep_mask_from_saliency(S, thr=0.25)
                    frames = [f for i, f in enumerate(frames) if keep[i]]
                    pal = self._build_global_palette(frames, colors=colors, seed=1234)
                    qframes = self._apply_global_palette(frames, pal, dither=True)

                iteration += 1

            # final best-effort return with metadata
            if last_meta is None:
                last_meta = {
                    'iteration': iteration,
                    'orig_fps': fps_in,
                    'orig_frames': orig_n,
                    'frames_out': len(qframes),
                    'colors': colors,
                    'fps_goal': fps,
                    'size_mb': round(size_mb, 4),
                    'total_ms': sum(durations_ms),
                    'durations_ms': durations_ms,
                    'preserve_timing_ok': abs(total_ms - sum(durations_ms)) <= 10
                }

            return data, last_meta

        except Exception as e:
            logger.error(f"Compress to target failed: {e}", exc_info=True)
            raise

    def estimate_compression_ratio(self, original_frames: List[Image.Image],
                                   compressed_frames: List[Image.Image]) -> dict:
        """
        Estimate compression metrics

        Returns:
            Dictionary with compression stats
        """
        if not original_frames or not compressed_frames:
            return {}

        try:
            # Estimate memory size
            orig_size = sum(f.size[0] * f.size[1] * 3 for f in original_frames)
            comp_size = sum(f.size[0] * f.size[1] * 3 for f in compressed_frames)

            return {
                'original_frames': len(original_frames),
                'compressed_frames': len(compressed_frames),
                'frame_reduction': f"{(1 - len(compressed_frames)/len(original_frames))*100:.1f}%",
                'size_reduction_estimate': f"{(1 - comp_size/orig_size)*100:.1f}%",
                'scale_factor': self.scale_factor,
                'technique': 'CWAM-inspired cross-window saliency'
            }
        except Exception as e:
            logger.error(f"Estimation failed: {e}")
            return {}


# Backward compatibility alias
GIFCompressor = CWAMInspiredCompressor
