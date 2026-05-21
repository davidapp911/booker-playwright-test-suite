# API Bug Log

Discrepancies found between the Swagger docs and the actual API behaviour during testing.

---

## POST /api/booking — Response shape does not match Swagger

**Swagger says:** Response is nested — `bookingid` at the top level with all booking fields inside a `booking` object.

**Actual:** Response is flat — `bookingid`, `roomid`, `firstname`, `lastname`, `depositpaid`, `bookingdates` all at the top level. No `booking` wrapper.

---

## POST /api/booking — Response omits email and phone

**Swagger says:** Response includes `email` and `phone`.

**Actual:** Neither field is returned in the POST response body. Both are accepted in the request but silently dropped from the response.

---

## PUT /api/booking/{id} — Response shape differs from POST

**Swagger says:** Consistent response shape across booking endpoints.

**Actual:** PUT returns the nested shape (`bookingid` + `booking` object) while POST returns a flat shape. The two endpoints are inconsistent with each other.

---

## PATCH /api/booking/{id} — Not documented in Swagger

**Swagger says:** No PATCH endpoint documented.

**Actual:** Endpoint may or may not exist — behaviour under investigation.

---

## POST /api/message — Response does not match documentation

**Docs say:** Response is the created message object including the assigned `id`.

**Actual:** Response is `{"success": true}` — no message object, no ID returned.

**Impact on testing:** ID-based verification after a UI contact form submission is not possible. Tests must fall back to listing all messages via `GET /api/message` and filtering by name to confirm persistence.

---

## DELETE /api/room/{id} — Bookings are not cascade deleted

**Expected:** Deleting a room removes all associated bookings, or the API rejects the deletion while active bookings exist.

**Actual:** The room is deleted but its bookings remain, referencing a room ID that no longer exists. No cascade delete is implemented.

**Impact on testing:** The `created_room` fixture deletes the room in teardown, leaving any bookings made against it as orphaned records. These can appear in subsequent `GET /api/booking?roomid=` calls if the room ID is recycled, polluting test results.

