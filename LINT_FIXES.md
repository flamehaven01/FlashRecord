# FlashRecord CI/CD Lint Fixes

## Remaining 11 Errors to Fix

### 1. compression.py:254 - B007
```python
# Before:
for i, f in enumerate(frames):

# After:
for _, f in enumerate(frames):
```

### 2. manager.py:27, 38, 48 - E722 (3 instances)
```python
# Before:
except:
    return 0

# After:
except Exception:
    return 0
```

### 3. manager.py:45 - B007
```python
# Before:
for root, _, files in os.walk(self.save_dir):

# After:
for _root, _, files in os.walk(self.save_dir):
```

### 4. api.py:96 - F841
```python
# Before:
result = cli.handle_command("screenshot", None)
if cli.recording_file:

# After:
cli.handle_command("screenshot", None)
if cli.recording_file:
```

### 5. api.py:107, 122, 139, 155, 170 - B904 (5 instances)
```python
# Before:
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

# After:
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e)) from e
```

## Quick Fix Commands

```bash
cd "D:/Sanctum/flashrecord"

# Fix compression.py
sed -i 's/for i, f in enumerate(frames):/for _, f in enumerate(frames):/g' src/flashrecord/compression.py

# Fix manager.py
sed -i 's/^        except:$/        except Exception:/g' src/flashrecord/manager.py
sed -i 's/for root, _, files in os.walk(self.save_dir):/for _root, _, files in os.walk(self.save_dir):/g' src/flashrecord/manager.py

# Fix api.py
sed -i 's/result = cli.handle_command/cli.handle_command/g' src/flashrecord/api.py
sed -i 's/raise HTTPException(status_code=500, detail=str(e))/raise HTTPException(status_code=500, detail=str(e)) from e/g' src/flashrecord/api.py
```

## Or Manual Fix (Recommended)

1. Open each file
2. Make the changes listed above
3. Run `ruff check src/` to verify
4. Run `black src/` to format
5. Commit and push
