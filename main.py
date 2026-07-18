import os
import json
import asyncio
from datetime import datetime, timedelta, timezone
import aiohttp

CONFIG_FILE = "config.json"

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        try:
            config = json.load(f)
            TOKEN = config.get("TOKEN", "")
            MY_USER_ID = config.get("MY_USER_ID", "")
            LANG = config.get("LANG", "")
        except:
            TOKEN = ""
            MY_USER_ID = ""
            LANG = ""
else:
    TOKEN = ""
    MY_USER_ID = ""
    LANG = ""

if not LANG:
    print("Dil Secin / Choose Language:")
    print("1. English")
    print("2. Turkce")
    lang_choice = input("Secim / Choice (1/2): ").strip()
    LANG = "tr" if lang_choice == "2" else "en"

def t(en_text, tr_text):
    return tr_text if LANG == "tr" else en_text

if not TOKEN:
    TOKEN = input(t("Discord token: ", "Discord token: ")).strip()
if not MY_USER_ID:
    MY_USER_ID = input(t("Your User ID: ", "Senin User ID'n: ")).strip()

with open(CONFIG_FILE, "w", encoding="utf-8") as f:
    json.dump({"TOKEN": TOKEN, "MY_USER_ID": MY_USER_ID, "LANG": LANG}, f, indent=4)

class DMCleaner:
    def __init__(self):
        self.headers = {
            "Authorization": TOKEN,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
        }
        self.base_url = "https://discord.com/api/v9"
        self.session = None
        self.my_user_id = MY_USER_ID

    def ask_days_limit(self):
        prompt = t("\nHow many days of messages do you want to delete? (0 for all): ", "\nKac gun icerisindeki mesajlari silmek istiyorsunuz? (Tumu icin 0): ")
        try:
            days_limit = int(input(prompt).strip() or "0")
        except ValueError:
            days_limit = 0
            
        if days_limit > 0:
            return datetime.now(timezone.utc) - timedelta(days=days_limit)
        return None

    async def start(self):
        print("starting...")
        self.session = aiohttp.ClientSession(headers=self.headers)
        
    
        async with self.session.get(f"{self.base_url}/users/@me") as resp:
            if resp.status != 200:
                print(f"bad token {resp.status}")
                await self.session.close()
                return
            me = await resp.json()
            print(f"logged in as {me['username']}")
            if self.my_user_id == "YOUR_USER_ID_HERE":
                self.my_user_id = me['id']
                print(f"got id {self.my_user_id}")
            else:
                print(f"my id {self.my_user_id}")
        
        print(t("\n--- Messages ---", "\n--- Mesaj Islemleri ---"))
        print(t("1. Export and delete specific ID messages", "1. Belirli bir ID'nin mesajlarini exportla ve sil"))
        print(t("2. Export specific ID messages only", "2. Belirli bir ID'nin mesajlarini sadece exportla"))
        print(t("3. Delete specific ID messages only", "3. Belirli bir ID'nin mesajlarini sadece sil"))
        print(t("4. Export all DMs", "4. Tum DM'leri exportla"))
        print(t("5. Delete my messages (open DMs)", "5. Sadece kendi mesajlarimi sil (Acik DM'ler)"))
        print(t("6. Export and delete my messages (open DMs)", "6. Kendi mesajlarimi exportla ve sil (Acik DM'ler)"))
        print(t("7. Delete all my messages (search api)", "7. Tum kendi mesajlarimi sil (Search API - Kapali DM'ler dahil)"))
        print(t("8. Export and delete all my messages (search api)", "8. Tum mesajlarimi exportla ve sil (Search API - Kapali DM'ler dahil)"))
        
        print(t("\n--- Social And Servers ---", "\n--- Sosyal ve Sunucu Islemleri ---"))
        print(t("9. Remove all friends", "9. Tum arkadaslari sil"))
        print(t("10. Cancel pending requests", "10. Bekleyen/gelen arkadaslik isteklerini iptal et"))
        print(t("11. Unblock all users", "11. Engellenen tum kullanicilarin engelini kaldir"))
        print(t("12. Leave all servers", "12. Tum sunuculardan cik"))
        print(t("13. Delete owned servers", "13. Sahibi oldugun sunuculari sil"))
        print(t("14. Leave all group DMs", "14. Tum grup DM'lerinden cik"))
        print(t("15. Close all open DMs", "15. Tum acik DM'leri kapat"))
        
        print(t("\n--- Account & Privacy ---", "\n--- Hesap ve Gizlilik ---"))
        print(t("16. Wipe profile (avatar, bio, etc)", "16. Profili sifirla (avatar, bio, vb)"))
        print(t("17. Remove connections (spotify, steam etc)", "17. Tum bagli hesaplari kaldir (spotify, steam vb)"))
        print(t("18. Revoke authorized apps (oauth)", "18. Yetkili uygulamalari (oauth) kaldir"))
        print(t("19. Leave hypesquad", "19. Hypesquad'dan cik"))
        
        print(t("\n20. Exit", "\n20. Cikis"))
        
        choice = input(t("\nChoice: ", "\nSecim: ")).strip()
        
        if choice == "1":
            await self.export_and_delete_specific_id()
        elif choice == "2":
            await self.export_specific_id()
        elif choice == "3":
            await self.delete_specific_id()
        elif choice == "4":
            await self.export_all_dms()
        elif choice == "5":
            await self.delete_my_messages()
        elif choice == "6":
            await self.export_and_delete()
        elif choice == "7":
            await self.delete_all_dms_via_search(export=False)
        elif choice == "8":
            await self.delete_all_dms_via_search(export=True)
        elif choice == "9":
            await self.remove_all_friends()
        elif choice == "10":
            await self.cancel_pending_requests()
        elif choice == "11":
            await self.unblock_all_users()
        elif choice == "12":
            await self.leave_all_servers()
        elif choice == "13":
            await self.delete_owned_servers()
        elif choice == "14":
            await self.leave_all_group_dms()
        elif choice == "15":
            await self.close_all_dms()
        elif choice == "16":
            await self.wipe_profile()
        elif choice == "17":
            await self.remove_connections()
        elif choice == "18":
            await self.revoke_authorized_apps()
        elif choice == "19":
            await self.leave_hypesquad()
        else:
            print("exiting...")
        
        await self.session.close()
        print("done")

    async def get_all_dm_channels(self):
        print("getting dms...")
        
        async with self.session.get(f"{self.base_url}/users/@me/channels") as resp:
            if resp.status != 200:
                print(f"error {resp.status}")
                return []
            channels = await resp.json()
        
        real_dms = []
        skipped = 0
        for ch in channels:
            if ch.get("is_message_request", False) or ch.get("type") == 12:
                skipped += 1
                continue
            if ch.get("type") in [1, 3]: 
                real_dms.append(ch)
        
        print(f"found {len(real_dms)} dms, skipped {skipped} requests")
        return real_dms

    async def search_messages_in_channel(self, channel_id, author_id=None, limit=500):
        all_messages = []
        offset = 0
        
        while True:
            params = {
                "channel_id": str(channel_id),
                "offset": offset,
                "limit": 50,
                "sort_by": "timestamp",
                "sort_order": "desc"
            }
            
            if author_id:
                params["author_id"] = str(author_id)
            
            async with self.session.get(f"{self.base_url}/channels/{channel_id}/messages/search", params=params) as resp:
                if resp.status != 200:
                    print(f"search api error {resp.status}")
                    break
                
                data = await resp.json()
                messages_data = data.get("messages", [])
                
                if not messages_data:
                    break
                
                for msg_group in messages_data:
                    for msg in msg_group:
                        all_messages.append(msg)
                
                offset += 50
                
                total = data.get("total_results", 0)
                if offset >= total or len(all_messages) >= total:
                    break
                
                await asyncio.sleep(0.3)
        
        return all_messages

    async def fetch_channel_messages(self, channel_id):
        all_messages = []
        before_id = None
        
        while True:
            params = {"limit": 100}
            if before_id:
                params["before"] = before_id
                
            async with self.session.get(f"{self.base_url}/channels/{channel_id}/messages", params=params) as resp:
                if resp.status == 429:
                    retry_after = float((await resp.json()).get("retry_after", 1))
                    await asyncio.sleep(retry_after + 1)
                    continue
                if resp.status != 200:
                    break
                    
                messages = await resp.json()
                if not messages:
                    break
                    
                all_messages.extend(messages)
                before_id = messages[-1]["id"]
                await asyncio.sleep(0.3)
                
        return all_messages

    async def get_user_info_from_channel(self, channel_data):
        ch_type = channel_data.get("type", 0)
        ch_id = channel_data["id"]
        
        if ch_type == 1 and channel_data.get("recipients"):
            r = channel_data["recipients"][0]
            return {
                "id": r.get("id", "bilinmiyor"),
                "username": r.get("username", "bilinmiyor"),
                "display_name": r.get("global_name") or r.get("username", "bilinmiyor"),
                "channel_id": ch_id,
                "type": "dm"
            }
        elif ch_type == 3:
            return {
                "id": f"grup_{ch_id}",
                "username": channel_data.get("name", f"GrupDM_{ch_id}"),
                "display_name": channel_data.get("name", f"GrupDM_{ch_id}"),
                "channel_id": ch_id,
                "type": "group"
            }
        else:
            return {
                "id": f"unknown_{ch_id}",
                "username": f"Bilinmeyen_{ch_id}",
                "display_name": f"Bilinmeyen_{ch_id}",
                "channel_id": ch_id,
                "type": "unknown"
            }

    async def export_all_dms(self):
        channels = await self.get_all_dm_channels()
        
        for ch in channels:
            user_info = await self.get_user_info_from_channel(ch)
            print(f"\nexporting {user_info['display_name']}")
            
            messages = await self.fetch_channel_messages(ch["id"])
            
            if not messages:
                print("no messages")
                continue
            
            safe_name = "".join(c for c in str(user_info['display_name']) if c.isalnum() or c in "._- ").strip()
            folder_name = f"{user_info['id']}_{safe_name}"
            base_path = os.path.join("dm_exports", folder_name)
            os.makedirs(base_path, exist_ok=True)
            
            metadata = {
                "user_id": user_info['id'],
                "username": user_info['username'],
                "display_name": user_info['display_name'],
                "channel_id": ch["id"],
                "channel_type": user_info['type'],
                "total_messages": len(messages),
                "export_date": datetime.now(timezone.utc).isoformat()
            }
            with open(os.path.join(base_path, "metadata.json"), "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            attachments_dir = os.path.join(base_path, "attachments")
            os.makedirs(attachments_dir, exist_ok=True)
            
            formatted_messages = []
            for msg in messages:
                msg_data = {
                    "id": msg["id"],
                    "timestamp": msg["timestamp"],
                    "author_id": msg["author"]["id"],
                    "author": msg["author"]["username"],
                    "content": msg.get("content", ""),
                    "attachments": []
                }
                
                for att in msg.get("attachments", []):
                    att_url = att.get("url", "")
                    att_name = att.get("filename", "file.bin")
                    safe_fname = f"{msg['id']}_{att['id']}.{att_name.split('.')[-1] if '.' in att_name else 'bin'}"
                    file_path = os.path.join(attachments_dir, safe_fname)
                    
                    try:
                        async with self.session.get(att_url) as att_resp:
                            if att_resp.status == 200:
                                with open(file_path, "wb") as f:
                                    f.write(await att_resp.read())
                    except:
                        pass
                    
                    msg_data["attachments"].append({
                        "original_name": att_name,
                        "saved_as": safe_fname,
                        "url": att_url
                    })
                
                formatted_messages.append(msg_data)
            
            with open(os.path.join(base_path, "messages.json"), "w", encoding="utf-8") as f:
                json.dump(formatted_messages, f, indent=2, ensure_ascii=False)
            
            txt_path = os.path.join(base_path, "messages.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"=== DM Konusmasi: {user_info['display_name']} ===\n")
                f.write(f"Kullanici ID: {user_info['id']}\n")
                f.write(f"Kanal ID: {ch['id']}\n")
                f.write(f"Toplam Mesaj: {len(formatted_messages)}\n")
                f.write(f"Tarih: {metadata['export_date']}\n")
                f.write("=" * 60 + "\n\n")
                
                sorted_msgs = sorted(formatted_messages, key=lambda x: x["timestamp"])
                for m in sorted_msgs:
                    ts = m["timestamp"][:19].replace("T", " ")
                    author = m["author"]
                    content = m["content"] if m["content"] else "(medya/ek)"
                    f.write(f"[{ts}] {author}:\n{content}\n")
                    if m["attachments"]:
                        for a in m["attachments"]:
                            f.write(f"    [Ek: {a['original_name']} -> {a['saved_as']}]\n")
                    f.write("\n")
            
            print(f"saved {len(formatted_messages)} messages")
            await asyncio.sleep(1)

    async def delete_my_messages(self):
        cutoff_date = self.ask_days_limit()

        channels = await self.get_all_dm_channels()
        
        total_deleted = 0
        total_failed = 0
        
        for ch in channels:
            user_info = await self.get_user_info_from_channel(ch)
            print(f"\ndeleting for {user_info['display_name']}")
            
            all_msgs = await self.fetch_channel_messages(ch["id"])
            my_messages_to_delete = []
            for m in all_msgs:
                if m.get("author", {}).get("id") == self.my_user_id:
                    if cutoff_date:
                        try:
                            msg_date = datetime.fromisoformat(m["timestamp"].replace("Z", "+00:00"))
                            if msg_date < cutoff_date:
                                continue
                        except:
                            pass
                    my_messages_to_delete.append(m)
            
            if not my_messages_to_delete:
                print("no messages found")
                continue
            
            print(f"deleting {len(my_messages_to_delete)} messages")
            
            deleted = 0
            failed = 0
            
            for msg in my_messages_to_delete:
                try:
                    delete_url = f"{self.base_url}/channels/{ch['id']}/messages/{msg['id']}"
                    async with self.session.delete(delete_url) as del_resp:
                        if del_resp.status in [200, 204]:
                            deleted += 1
                            if deleted % 10 == 0:
                                print(f"deleted {deleted}/{len(my_messages_to_delete)}")
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(0.5)
                        elif del_resp.status == 429:
                            retry_after = float((await del_resp.json()).get("retry_after", 1))
                            print(f"rate limit {retry_after}s")
                            await asyncio.sleep(retry_after + 1)
                        elif del_resp.status == 403:
                            failed += 1
                            if failed == 1:
                                print("cannot delete older than 14 days")
                        else:
                            failed += 1
                except:
                    failed += 1
            
            print(f"deleted {deleted}, failed {failed}")
            total_deleted += deleted
            total_failed += failed
            await asyncio.sleep(1)
        
        print(f"\ntotal deleted: {total_deleted}, total failed: {total_failed}")

    async def export_and_delete(self):
        cutoff_date = self.ask_days_limit()

        channels = await self.get_all_dm_channels()
        
        total_deleted = 0
        total_failed = 0
        
        for ch in channels:
            user_info = await self.get_user_info_from_channel(ch)
            print(f"\nprocessing {user_info['display_name']}")
            
            all_messages = await self.fetch_channel_messages(ch["id"])
            
            if not all_messages:
                print("no messages")
                continue

            safe_name = "".join(c for c in str(user_info['display_name']) if c.isalnum() or c in "._- ").strip()
            folder_name = f"{user_info['id']}_{safe_name}"
            base_path = os.path.join("dm_exports", folder_name)
            os.makedirs(base_path, exist_ok=True)
            
            metadata = {
                "user_id": user_info['id'],
                "username": user_info['username'],
                "display_name": user_info['display_name'],
                "channel_id": ch["id"],
                "channel_type": user_info['type'],
                "total_messages": len(all_messages),
                "export_date": datetime.now(timezone.utc).isoformat()
            }
            with open(os.path.join(base_path, "metadata.json"), "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            attachments_dir = os.path.join(base_path, "attachments")
            os.makedirs(attachments_dir, exist_ok=True)
            
            formatted_messages = []
            my_message_ids_to_delete = []
            
            for msg in all_messages:
                msg_data = {
                    "id": msg["id"],
                    "timestamp": msg["timestamp"],
                    "author_id": msg["author"]["id"],
                    "author": msg["author"]["username"],
                    "content": msg.get("content", ""),
                    "attachments": []
                }
                
                for att in msg.get("attachments", []):
                    att_url = att.get("url", "")
                    att_name = att.get("filename", "file.bin")
                    safe_fname = f"{msg['id']}_{att['id']}.{att_name.split('.')[-1] if '.' in att_name else 'bin'}"
                    file_path = os.path.join(attachments_dir, safe_fname)
                    
                    try:
                        async with self.session.get(att_url) as att_resp:
                            if att_resp.status == 200:
                                with open(file_path, "wb") as f:
                                    f.write(await att_resp.read())
                    except:
                        pass
                    
                    msg_data["attachments"].append({
                        "original_name": att_name,
                        "saved_as": safe_fname,
                        "url": att_url
                    })
                
                formatted_messages.append(msg_data)
                
                if msg["author"]["id"] == self.my_user_id:
                    if cutoff_date:
                        try:
                            msg_date = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
                            if msg_date < cutoff_date:
                                continue
                        except:
                            pass
                    my_message_ids_to_delete.append(msg["id"])
            
            with open(os.path.join(base_path, "messages.json"), "w", encoding="utf-8") as f:
                json.dump(formatted_messages, f, indent=2, ensure_ascii=False)
            
            txt_path = os.path.join(base_path, "messages.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"=== DM Konuşması: {user_info['display_name']} ===\n")
                f.write(f"Kullanıcı ID: {user_info['id']}\n")
                f.write(f"Kanal ID: {ch['id']}\n")
                f.write(f"Toplam Mesaj: {len(formatted_messages)}\n")
                f.write(f"Tarih: {metadata['export_date']}\n")
                f.write("=" * 60 + "\n\n")
                
                sorted_msgs = sorted(formatted_messages, key=lambda x: x["timestamp"])
                for m in sorted_msgs:
                    ts = m["timestamp"][:19].replace("T", " ")
                    author = m["author"]
                    content = m["content"] if m["content"] else "(medya/ek)"
                    f.write(f"[{ts}] {author}:\n{content}\n")
                    if m["attachments"]:
                        for a in m["attachments"]:
                            f.write(f"    [Ek: {a['original_name']} -> {a['saved_as']}]\n")
                    f.write("\n")
            
            print(f"saved {len(formatted_messages)} messages")
            
            if my_message_ids_to_delete:
                print(f"     {len(my_message_ids_to_delete)} kendi mesajın siliniyor...")
                
                deleted = 0
                failed = 0
                
                for msg_id in my_message_ids_to_delete:
                    try:
                        delete_url = f"{self.base_url}/channels/{ch['id']}/messages/{msg_id}"
                        async with self.session.delete(delete_url) as del_resp:
                            if del_resp.status in [200, 204]:
                                deleted += 1
                                if deleted % 10 == 0:
                                    print(f"         {deleted}/{len(my_message_ids_to_delete)}")
                                    await asyncio.sleep(2)
                                else:
                                    await asyncio.sleep(0.5)
                            elif del_resp.status == 429:
                                retry_after = float((await del_resp.json()).get("retry_after", 1))
                                print(f"rate limit {retry_after}s")
                                await asyncio.sleep(retry_after + 1)
                            elif del_resp.status == 403:
                                failed += 1
                                if failed == 1:
                                    print("cannot delete older than 14 days")
                            else:
                                failed += 1
                    except:
                        failed += 1
                
                print(f"deleted {deleted}, failed {failed}")
                total_deleted += deleted
                total_failed += failed
            else:
                print("no messages to delete")
            
            await asyncio.sleep(1)
        print(f"\ntotal deleted: {total_deleted}, total failed: {total_failed}")

    async def delete_all_dms_via_search(self, export=False):
        if not self.my_user_id:
            print("my id missing")
            return
            
        cutoff_date = self.ask_days_limit()

        print("\nsearching all dms...")
        if export:
            print("exporting messages first")
        print("fetching pages...")
        
        total_deleted = 0
        total_failed = 0
        channels_data = []
        exported_channels = set()
        
        while True:
            offset = 0
            page_has_results = True
            deleted_in_pass = 0
            
            while page_has_results:
                payload = {
                    "tabs": {
                        "messages": {
                            "sort_by": "timestamp",
                            "sort_order": "desc",
                            "author_id": [str(self.my_user_id)],
                            "offset": offset,
                            "limit": 25
                        }
                    },
                    "track_exact_total_hits": True
                }
                
                async with self.session.post(f"{self.base_url}/users/@me/messages/search/tabs", json=payload) as resp:
                    if resp.status == 429:
                        retry_after = float((await resp.json()).get("retry_after", 2))
                        print(f"rate limit search {retry_after}s")
                        await asyncio.sleep(retry_after + 1)
                        continue
                        
                    if resp.status == 202:
                        try:
                            retry_after = float((await resp.json()).get("retry_after", 5))
                        except:
                            retry_after = 5
                        print(f"indexing wait {retry_after}s")
                        await asyncio.sleep(retry_after)
                        continue
                        
                    if resp.status != 200:
                        print(f"search api err {resp.status}")
                        page_has_results = False
                        break
                    
                    data = await resp.json()
                    tabs_messages = data.get("tabs", {}).get("messages", {})
                    messages_data = tabs_messages.get("messages", [])
                    channels_data = tabs_messages.get("channels", [])
                    total_results = tabs_messages.get("total_results", 0)
                    
                    if offset == 0:
                        print(f"\ntotal {total_results} messages")
                    
                    if not messages_data:
                        page_has_results = False
                        break
                    
                    my_messages = []
                    for msg_group in messages_data:
                        for msg in msg_group:
                            if msg.get("author", {}).get("id") == str(self.my_user_id):
                                if not any(m["id"] == msg["id"] for m in my_messages):
                                    if cutoff_date:
                                        try:
                                            msg_date = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
                                            if msg_date < cutoff_date:
                                                page_has_results = False
                                                continue
                                        except:
                                            pass
                                    my_messages.append(msg)
                    
                    if not my_messages:
                        if not page_has_results:
                            break
                        print(f"offset {offset} empty")
                        offset += 25
                        await asyncio.sleep(1)
                        continue
                    
                    print(f"offset {offset}: {len(my_messages)} to delete")
                    
                    for msg in my_messages:
                        ch_id = msg.get("channel_id")
                        msg_id = msg.get("id")
                        
                        if export and ch_id not in exported_channels:
                            exported_channels.add(ch_id)
                            recipient_name = "Unknown"
                            for ch in channels_data:
                                if ch.get("id") == ch_id:
                                    recipients = ch.get("recipients", [])
                                    if recipients:
                                        recipient_name = recipients[0].get("username", "Unknown")
                                    break
                                    
                            safe_name = "".join(c for c in recipient_name if c.isalnum() or c in "._- ").strip()
                            folder_name = f"{ch_id}_{safe_name}"
                            base_path = os.path.join("dm_exports", "search_exports", folder_name)
                            os.makedirs(base_path, exist_ok=True)
                            
                            print(f"fetching all messages for channel: {recipient_name}...")
                            channel_messages = await self.fetch_channel_messages(ch_id)
                            
                            attachments_dir = os.path.join(base_path, "attachments")
                            os.makedirs(attachments_dir, exist_ok=True)
                            
                            formatted_messages = []
                            for c_msg in channel_messages:
                                msg_data = {
                                    "id": c_msg["id"],
                                    "timestamp": c_msg.get("timestamp"),
                                    "author_id": c_msg.get("author", {}).get("id"),
                                    "author": c_msg.get("author", {}).get("username"),
                                    "content": c_msg.get("content", ""),
                                    "attachments": []
                                }
                                
                                for att in c_msg.get("attachments", []):
                                    att_url = att.get("url", "")
                                    att_name = att.get("filename", "file.bin")
                                    safe_fname = f"{c_msg['id']}_{att.get('id', 'x')}.{att_name.split('.')[-1] if '.' in att_name else 'bin'}"
                                    file_path = os.path.join(attachments_dir, safe_fname)
                                    
                                    try:
                                        async with self.session.get(att_url) as att_resp:
                                            if att_resp.status == 200:
                                                with open(file_path, "wb") as f:
                                                    f.write(await att_resp.read())
                                    except:
                                        pass
                                    
                                    msg_data["attachments"].append({
                                        "original_name": att_name,
                                        "saved_as": safe_fname,
                                        "url": att_url
                                    })
                                formatted_messages.append(msg_data)
                            
                            messages_file = os.path.join(base_path, "messages.json")
                            with open(messages_file, "w", encoding="utf-8") as f:
                                json.dump(formatted_messages, f, indent=2, ensure_ascii=False)
                                
                            txt_path = os.path.join(base_path, "messages.txt")
                            with open(txt_path, "w", encoding="utf-8") as f:
                                f.write(f"=== DM Konusmasi: {recipient_name} ===\n")
                                f.write(f"Kanal ID: {ch_id}\n")
                                f.write(f"Toplam Mesaj: {len(formatted_messages)}\n")
                                f.write("=" * 60 + "\n\n")
                                
                                sorted_msgs = sorted(formatted_messages, key=lambda x: x["timestamp"])
                                for m in sorted_msgs:
                                    ts = m["timestamp"][:19].replace("T", " ")
                                    author = m["author"]
                                    content = m["content"] if m["content"] else "(medya/ek)"
                                    f.write(f"[{ts}] {author}:\n{content}\n")
                                    if m["attachments"]:
                                        for a in m["attachments"]:
                                            f.write(f"    [Ek: {a['original_name']} -> {a['saved_as']}]\n")
                                    f.write("\n")
                            print(f"logged {len(formatted_messages)} messages.")
                        
                        delete_url = f"{self.base_url}/channels/{ch_id}/messages/{msg_id}"
                        try:
                            async with self.session.delete(delete_url) as del_resp:
                                if del_resp.status in [200, 204]:
                                    deleted_in_pass += 1
                                    total_deleted += 1
                                    print(f"deleted msg {msg_id}")
                                    await asyncio.sleep(1.2)
                                elif del_resp.status == 429:
                                    try:
                                        retry_after = float((await del_resp.json()).get("retry_after", 2))
                                    except:
                                        retry_after = 2
                                    print(f"rate limit del {retry_after}s")
                                    await asyncio.sleep(retry_after + 1)
                                elif del_resp.status == 404:
                                    pass
                                else:
                                    total_failed += 1
                        except Exception as e:
                            total_failed += 1
                    
                    offset += 25
                    await asyncio.sleep(2)
            
            if deleted_in_pass == 0:
                print("\ndelete finish")
                break
            else:
                print("\nwaiting 5s for index...")
                await asyncio.sleep(5)
                
        print(f"\nfinish. deleted: {total_deleted}, failed: {total_failed}")

    async def get_relationships(self):
        async with self.session.get(f"{self.base_url}/users/@me/relationships") as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                err = await resp.text()
                print(f"failed to get relationships. Status: {resp.status}, Error: {err[:100]}")
            return []

    async def remove_all_friends(self):
        print("\ngetting relationships...")
        rels = await self.get_relationships()
        friends = [r for r in rels if r.get("type") == 1]
        
        if not friends:
            print("no friends found.")
            return

        print(f"found {len(friends)} friends to remove.")
        for f in friends:
            user_id = f["id"]
            username = f.get("user", {}).get("username", "unknown")
            while True:
                async with self.session.delete(f"{self.base_url}/users/@me/relationships/{user_id}") as resp:
                    if resp.status in [200, 204]:
                        print(f"removed friend {username}")
                        break
                    elif resp.status == 429:
                        try: retry = float((await resp.json()).get("retry_after", 1))
                        except: retry = 1
                        print(f"rate limit, waiting {retry}s")
                        await asyncio.sleep(retry + 0.5)
                    else:
                        print(f"failed to remove {username} (status: {resp.status})")
                        break
            await asyncio.sleep(1)
        print("finished removing friends.")

    async def unblock_all_users(self):
        print("\ngetting relationships...")
        rels = await self.get_relationships()
        blocked = [r for r in rels if r.get("type") == 2]
        
        if not blocked:
            print("no blocked users found.")
            return

        print(f"found {len(blocked)} blocked users to unblock.")
        for b in blocked:
            user_id = b["id"]
            username = b.get("user", {}).get("username", "unknown")
            while True:
                async with self.session.delete(f"{self.base_url}/users/@me/relationships/{user_id}") as resp:
                    if resp.status in [200, 204]:
                        print(f"unblocked user {username}")
                        break
                    elif resp.status == 429:
                        try: retry = float((await resp.json()).get("retry_after", 1))
                        except: retry = 1
                        print(f"rate limit, waiting {retry}s")
                        await asyncio.sleep(retry + 0.5)
                    else:
                        print(f"failed to unblock {username} (status: {resp.status})")
                        break
            await asyncio.sleep(1)
        print("finished unblocking users.")

    async def get_guilds(self):
        async with self.session.get(f"{self.base_url}/users/@me/guilds") as resp:
            if resp.status == 200:
                return await resp.json()
            return []

    async def leave_all_servers(self):
        print("\ngetting servers...")
        guilds = await self.get_guilds()
        
        to_leave = [g for g in guilds if not g.get("owner")]
        
        if not to_leave:
            print("no servers to leave (or you own them all).")
            return
            
        print(f"found {len(to_leave)} servers to leave.")
        for g in to_leave:
            guild_id = g["id"]
            name = g.get("name", "unknown")
            while True:
                async with self.session.delete(f"{self.base_url}/users/@me/guilds/{guild_id}", json={"lurking": False}) as resp:
                    if resp.status in [200, 204]:
                        print(f"left server {name}")
                        break
                    elif resp.status == 429:
                        try: retry = float((await resp.json()).get("retry_after", 1))
                        except: retry = 1
                        print(f"rate limit, waiting {retry}s")
                        await asyncio.sleep(retry + 0.5)
                    elif resp.status == 400:
                        err_text = await resp.text()
                        print(f"failed to leave {name} (400: {err_text[:50]})")
                        break
                    else:
                        print(f"failed to leave {name} (status: {resp.status})")
                        break
            await asyncio.sleep(1.5)
        print("finished leaving servers.")

    async def delete_owned_servers(self):
        print("\ngetting servers...")
        guilds = await self.get_guilds()
        
        owned = [g for g in guilds if g.get("owner")]
        
        if not owned:
            print("no owned servers found.")
            return
            
        print(f"found {len(owned)} servers you own to delete.")
        for g in owned:
            guild_id = g["id"]
            name = g.get("name", "unknown")
            while True:
                async with self.session.post(f"{self.base_url}/guilds/{guild_id}/delete", json={}) as resp:
                    if resp.status in [200, 204]:
                        print(f"deleted server {name}")
                        break
                    elif resp.status == 429:
                        try: retry = float((await resp.json()).get("retry_after", 1))
                        except: retry = 1
                        print(f"rate limit, waiting {retry}s")
                        await asyncio.sleep(retry + 0.5)
                    else:
                        err_text = await resp.text()
                        if resp.status == 400 and 'mfa' in err_text.lower():
                            print(f"failed to delete {name} (MFA/2FA required)")
                        else:
                            print(f"failed to delete {name} (status: {resp.status})")
                        break
            await asyncio.sleep(2)
        print("finished deleting owned servers.")

    async def leave_all_group_dms(self):
        print("\ngetting channels...")
        async with self.session.get(f"{self.base_url}/users/@me/channels") as resp:
            if resp.status != 200:
                print("failed to get channels.")
                return
            channels = await resp.json()
            
        groups = [c for c in channels if c.get("type") == 3]
        
        if not groups:
            print("no group dms found.")
            return
            
        print(f"found {len(groups)} group dms to leave.")
        for c in groups:
            channel_id = c["id"]
            name = c.get("name") or "Unnamed Group"
            while True:
                async with self.session.delete(f"{self.base_url}/channels/{channel_id}") as resp:
                    if resp.status in [200, 204]:
                        print(f"left group dm {name}")
                        break
                    elif resp.status == 429:
                        try: retry = float((await resp.json()).get("retry_after", 1))
                        except: retry = 1
                        print(f"rate limit, waiting {retry}s")
                        await asyncio.sleep(retry + 0.5)
                    else:
                        print(f"failed to leave group dm {name} (status: {resp.status})")
                        break
            await asyncio.sleep(1)
        print("finished leaving group dms.")

    async def close_all_dms(self):
        print("\ngetting channels...")
        async with self.session.get(f"{self.base_url}/users/@me/channels") as resp:
            if resp.status != 200:
                print("failed to get channels.")
                return
            channels = await resp.json()
            
        dms = [c for c in channels if c.get("type") == 1]
        
        if not dms:
            print("no open dms found.")
            return
            
        print(f"found {len(dms)} open dms to close.")
        for c in dms:
            channel_id = c["id"]
            recipient = c.get("recipients", [{}])[0].get("username", "unknown")
            while True:
                async with self.session.delete(f"{self.base_url}/channels/{channel_id}") as resp:
                    if resp.status in [200, 204]:
                        print(f"closed dm with {recipient}")
                        break
                    elif resp.status == 429:
                        try: retry = float((await resp.json()).get("retry_after", 1))
                        except: retry = 1
                        print(f"rate limit, waiting {retry}s")
                        await asyncio.sleep(retry + 0.5)
                    else:
                        print(f"failed to close dm with {recipient} (status: {resp.status})")
                        break
            await asyncio.sleep(1)
        print("finished closing dms.")

    async def cancel_pending_requests(self):
        print("\ngetting relationships...")
        rels = await self.get_relationships()
        pending = [r for r in rels if r.get("type") in [3, 4]]
        
        if not pending:
            print("no pending requests found.")
            return

        print(f"found {len(pending)} pending requests to cancel.")
        for r in pending:
            user_id = r["id"]
            username = r.get("user", {}).get("username", "unknown")
            while True:
                async with self.session.delete(f"{self.base_url}/users/@me/relationships/{user_id}") as resp:
                    if resp.status in [200, 204]:
                        print(f"canceled request for {username}")
                        break
                    elif resp.status == 429:
                        try: retry = float((await resp.json()).get("retry_after", 1))
                        except: retry = 1
                        print(f"rate limit, waiting {retry}s")
                        await asyncio.sleep(retry + 0.5)
                    else:
                        print(f"failed to cancel {username} (status: {resp.status})")
                        break
            await asyncio.sleep(1)
        print("finished canceling pending requests.")

    async def wipe_profile(self):
        print("\nwiping profile (avatar, banner, bio, custom status)...")
        payload = {"avatar": None, "banner": None, "bio": ""}
        async with self.session.patch(f"{self.base_url}/users/@me", json=payload) as resp:
            if resp.status == 200:
                print("cleared avatar, banner, and bio.")
            else:
                print(f"failed to clear profile info (status: {resp.status})")
        
        await asyncio.sleep(1)
        
        settings_payload = {"custom_status": None}
        async with self.session.patch(f"{self.base_url}/users/@me/settings", json=settings_payload) as resp:
            if resp.status == 200:
                print("cleared custom status.")
            else:
                print(f"failed to clear custom status (status: {resp.status})")
                
        print("finished wiping profile.")

    async def remove_connections(self):
        print("\ngetting connections...")
        async with self.session.get(f"{self.base_url}/users/@me/connections") as resp:
            if resp.status != 200:
                print(f"failed to get connections (status: {resp.status})")
                return
            connections = await resp.json()
            
        if not connections:
            print("no connections found.")
            return
            
        print(f"found {len(connections)} connections to remove.")
        for c in connections:
            conn_type = c.get("type")
            conn_id = c.get("id")
            name = c.get("name")
            
            while True:
                async with self.session.delete(f"{self.base_url}/users/@me/connections/{conn_type}/{conn_id}") as resp:
                    if resp.status in [200, 204]:
                        print(f"removed connection {name} ({conn_type})")
                        break
                    elif resp.status == 429:
                        try: retry = float((await resp.json()).get("retry_after", 1))
                        except: retry = 1
                        print(f"rate limit, waiting {retry}s")
                        await asyncio.sleep(retry + 0.5)
                    else:
                        print(f"failed to remove {name} (status: {resp.status})")
                        break
            await asyncio.sleep(1)
        print("finished removing connections.")

    async def revoke_authorized_apps(self):
        print("\ngetting authorized apps...")
        async with self.session.get(f"{self.base_url}/oauth2/tokens") as resp:
            if resp.status != 200:
                print(f"failed to get authorized apps (status: {resp.status}).")
                return
            tokens = await resp.json()
            
        if not tokens:
            print("no authorized apps found.")
            return
            
        print(f"found {len(tokens)} authorized apps to revoke.")
        for t in tokens:
            auth_id = t.get("id")
            app_name = t.get("application", {}).get("name", "Unknown App")
            
            while True:
                async with self.session.delete(f"{self.base_url}/oauth2/tokens/{auth_id}") as resp:
                    if resp.status in [200, 204]:
                        print(f"revoked app {app_name}")
                        break
                    elif resp.status == 429:
                        try: retry = float((await resp.json()).get("retry_after", 1))
                        except: retry = 1
                        print(f"rate limit, waiting {retry}s")
                        await asyncio.sleep(retry + 0.5)
                    else:
                        print(f"failed to revoke {app_name} (status: {resp.status})")
                        break
            await asyncio.sleep(1)
        print("finished revoking authorized apps.")

    async def leave_hypesquad(self):
        print("\nleaving hypesquad...")
        async with self.session.delete(f"{self.base_url}/hypesquad/online") as resp:
            if resp.status in [200, 204]:
                print("successfully left hypesquad.")
            elif resp.status == 404:
                print("you are not in hypesquad.")
            else:
                print(f"failed to leave hypesquad (status: {resp.status})")

    async def export_and_delete_specific_id(self):
        target_id = input("\nLütfen export/delete atmak istediğiniz kullanicinin ID'sini girin: ").strip()
        if not target_id:
            print("ID boş olamaz.")
            return

        cutoff_date = self.ask_days_limit()
            
        channels = await self.get_all_dm_channels()
        target_ch = None
        for ch in channels:
            if ch.get("type") == 1 and ch.get("recipients"):
                if ch["recipients"][0].get("id") == target_id:
                    target_ch = ch
                    break
        
        if not target_ch:
            print(f"{target_id} ID'li kullanici ile acik bir DM bulunamadi.")
            return
            
        user_info = await self.get_user_info_from_channel(target_ch)
        print(f"\nprocessing {user_info['display_name']} (ID: {target_id})")
        
        all_messages = await self.fetch_channel_messages(target_ch["id"])
        
        if not all_messages:
            print("no messages")
            return

        safe_name = "".join(c for c in str(user_info['display_name']) if c.isalnum() or c in "._- ").strip()
        folder_name = f"{user_info['id']}_{safe_name}"
        base_path = os.path.join("dm_exports", folder_name)
        os.makedirs(base_path, exist_ok=True)
        
        metadata = {
            "user_id": user_info['id'],
            "username": user_info['username'],
            "display_name": user_info['display_name'],
            "channel_id": target_ch["id"],
            "channel_type": user_info['type'],
            "total_messages": len(all_messages),
            "export_date": datetime.now(timezone.utc).isoformat()
        }
        with open(os.path.join(base_path, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        attachments_dir = os.path.join(base_path, "attachments")
        os.makedirs(attachments_dir, exist_ok=True)
        
        formatted_messages = []
        my_message_ids_to_delete = []
        
        for msg in all_messages:
            msg_data = {
                "id": msg["id"],
                "timestamp": msg["timestamp"],
                "author_id": msg["author"]["id"],
                "author": msg["author"]["username"],
                "content": msg.get("content", ""),
                "attachments": []
            }
            
            for att in msg.get("attachments", []):
                att_url = att.get("url", "")
                att_name = att.get("filename", "file.bin")
                safe_fname = f"{msg['id']}_{att['id']}.{att_name.split('.')[-1] if '.' in att_name else 'bin'}"
                file_path = os.path.join(attachments_dir, safe_fname)
                
                try:
                    async with self.session.get(att_url) as att_resp:
                        if att_resp.status == 200:
                            with open(file_path, "wb") as f:
                                f.write(await att_resp.read())
                except:
                    pass
                
                msg_data["attachments"].append({
                    "original_name": att_name,
                    "saved_as": safe_fname,
                    "url": att_url
                })
            
            formatted_messages.append(msg_data)
            
            if msg["author"]["id"] == self.my_user_id:
                if cutoff_date:
                    try:
                        msg_date = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
                        if msg_date < cutoff_date:
                            continue
                    except:
                        pass
                my_message_ids_to_delete.append(msg["id"])
        
        with open(os.path.join(base_path, "messages.json"), "w", encoding="utf-8") as f:
            json.dump(formatted_messages, f, indent=2, ensure_ascii=False)
        
        txt_path = os.path.join(base_path, "messages.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"=== DM Konusmasi: {user_info['display_name']} ===\n")
            f.write(f"Kullanici ID: {user_info['id']}\n")
            f.write(f"Kanal ID: {target_ch['id']}\n")
            f.write(f"Toplam Mesaj: {len(formatted_messages)}\n")
            f.write(f"Tarih: {metadata['export_date']}\n")
            f.write("=" * 60 + "\n\n")
            
            sorted_msgs = sorted(formatted_messages, key=lambda x: x["timestamp"])
            for m in sorted_msgs:
                ts = m["timestamp"][:19].replace("T", " ")
                author = m["author"]
                content = m["content"] if m["content"] else "(medya/ek)"
                f.write(f"[{ts}] {author}:\n{content}\n")
                if m["attachments"]:
                    for a in m["attachments"]:
                        f.write(f"    [Ek: {a['original_name']} -> {a['saved_as']}]\n")
                f.write("\n")
        
        print(f"saved {len(formatted_messages)} messages")
        
        if my_message_ids_to_delete:
            print(f"     {len(my_message_ids_to_delete)} kendi mesajın siliniyor...")
            
            deleted = 0
            failed = 0
            
            for msg_id in my_message_ids_to_delete:
                try:
                    delete_url = f"{self.base_url}/channels/{target_ch['id']}/messages/{msg_id}"
                    async with self.session.delete(delete_url) as del_resp:
                        if del_resp.status in [200, 204]:
                            deleted += 1
                            if deleted % 10 == 0:
                                print(f"         {deleted}/{len(my_message_ids_to_delete)}")
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(0.5)
                        elif del_resp.status == 429:
                            try:
                                retry_after = float((await del_resp.json()).get("retry_after", 1))
                            except:
                                retry_after = 1
                            print(f"rate limit {retry_after}s")
                            await asyncio.sleep(retry_after + 1)
                        else:
                            failed += 1
                except:
                    failed += 1
            
            print(f"deleted {deleted}, failed {failed}")
        else:
            print("no messages to delete")

    async def export_specific_id(self):
        target_id = input("\nLütfen sadece export atmak istediğiniz kullanicinin ID'sini girin: ").strip()
        if not target_id:
            print("ID boş olamaz.")
            return
            
        channels = await self.get_all_dm_channels()
        target_ch = None
        for ch in channels:
            if ch.get("type") == 1 and ch.get("recipients"):
                if ch["recipients"][0].get("id") == target_id:
                    target_ch = ch
                    break
        
        if not target_ch:
            print(f"{target_id} ID'li kullanici ile acik bir DM bulunamadi.")
            return
            
        user_info = await self.get_user_info_from_channel(target_ch)
        print(f"\nprocessing {user_info['display_name']} (ID: {target_id})")
        
        all_messages = await self.fetch_channel_messages(target_ch["id"])
        
        if not all_messages:
            print("no messages")
            return

        safe_name = "".join(c for c in str(user_info['display_name']) if c.isalnum() or c in "._- ").strip()
        folder_name = f"{user_info['id']}_{safe_name}"
        base_path = os.path.join("dm_exports", folder_name)
        os.makedirs(base_path, exist_ok=True)
        
        metadata = {
            "user_id": user_info['id'],
            "username": user_info['username'],
            "display_name": user_info['display_name'],
            "channel_id": target_ch["id"],
            "channel_type": user_info['type'],
            "total_messages": len(all_messages),
            "export_date": datetime.now(timezone.utc).isoformat()
        }
        with open(os.path.join(base_path, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        attachments_dir = os.path.join(base_path, "attachments")
        os.makedirs(attachments_dir, exist_ok=True)
        
        formatted_messages = []
        
        for msg in all_messages:
            msg_data = {
                "id": msg["id"],
                "timestamp": msg["timestamp"],
                "author_id": msg["author"]["id"],
                "author": msg["author"]["username"],
                "content": msg.get("content", ""),
                "attachments": []
            }
            
            for att in msg.get("attachments", []):
                att_url = att.get("url", "")
                att_name = att.get("filename", "file.bin")
                safe_fname = f"{msg['id']}_{att['id']}.{att_name.split('.')[-1] if '.' in att_name else 'bin'}"
                file_path = os.path.join(attachments_dir, safe_fname)
                
                try:
                    async with self.session.get(att_url) as att_resp:
                        if att_resp.status == 200:
                            with open(file_path, "wb") as f:
                                f.write(await att_resp.read())
                except:
                    pass
                
                msg_data["attachments"].append({
                    "original_name": att_name,
                    "saved_as": safe_fname,
                    "url": att_url
                })
            
            formatted_messages.append(msg_data)
        
        with open(os.path.join(base_path, "messages.json"), "w", encoding="utf-8") as f:
            json.dump(formatted_messages, f, indent=2, ensure_ascii=False)
        
        txt_path = os.path.join(base_path, "messages.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"=== DM Konusmasi: {user_info['display_name']} ===\n")
            f.write(f"Kullanici ID: {user_info['id']}\n")
            f.write(f"Kanal ID: {target_ch['id']}\n")
            f.write(f"Toplam Mesaj: {len(formatted_messages)}\n")
            f.write(f"Tarih: {metadata['export_date']}\n")
            f.write("=" * 60 + "\n\n")
            
            sorted_msgs = sorted(formatted_messages, key=lambda x: x["timestamp"])
            for m in sorted_msgs:
                ts = m["timestamp"][:19].replace("T", " ")
                author = m["author"]
                content = m["content"] if m["content"] else "(medya/ek)"
                f.write(f"[{ts}] {author}:\n{content}\n")
                if m["attachments"]:
                    for a in m["attachments"]:
                        f.write(f"    [Ek: {a['original_name']} -> {a['saved_as']}]\n")
                f.write("\n")
        
        print(f"saved {len(formatted_messages)} messages")

    async def delete_specific_id(self):
        target_id = input("\nLütfen sadece silme yapmak istediğiniz kullanicinin ID'sini girin: ").strip()
        if not target_id:
            print("ID boş olamaz.")
            return

        cutoff_date = self.ask_days_limit()
            
        channels = await self.get_all_dm_channels()
        target_ch = None
        for ch in channels:
            if ch.get("type") == 1 and ch.get("recipients"):
                if ch["recipients"][0].get("id") == target_id:
                    target_ch = ch
                    break
        
        if not target_ch:
            print(f"{target_id} ID'li kullanici ile acik bir DM bulunamadi.")
            return
            
        user_info = await self.get_user_info_from_channel(target_ch)
        print(f"\nprocessing {user_info['display_name']} (ID: {target_id})")
        
        all_messages = await self.fetch_channel_messages(target_ch["id"])
        
        if not all_messages:
            print("no messages")
            return
            
        my_message_ids_to_delete = []
        for msg in all_messages:
            if msg.get("author", {}).get("id") == self.my_user_id:
                if cutoff_date:
                    try:
                        msg_date = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
                        if msg_date < cutoff_date:
                            continue
                    except:
                        pass
                my_message_ids_to_delete.append(msg["id"])
                
        if my_message_ids_to_delete:
            print(f"     {len(my_message_ids_to_delete)} kendi mesajin siliniyor...")
            
            deleted = 0
            failed = 0
            
            for msg_id in my_message_ids_to_delete:
                try:
                    delete_url = f"{self.base_url}/channels/{target_ch['id']}/messages/{msg_id}"
                    async with self.session.delete(delete_url) as del_resp:
                        if del_resp.status in [200, 204]:
                            deleted += 1
                            if deleted % 10 == 0:
                                print(f"         {deleted}/{len(my_message_ids_to_delete)}")
                                await asyncio.sleep(2)
                            else:
                                await asyncio.sleep(0.5)
                        elif del_resp.status == 429:
                            try:
                                retry_after = float((await del_resp.json()).get("retry_after", 1))
                            except:
                                retry_after = 1
                            print(f"rate limit {retry_after}s")
                            await asyncio.sleep(retry_after + 1)
                        else:
                            failed += 1
                except:
                    failed += 1
            
            print(f"deleted {deleted}, failed {failed}")
        else:
            print("no messages to delete")

async def main():
    cleaner = DMCleaner()
    await cleaner.start()

if __name__ == "__main__":
    asyncio.run(main())
