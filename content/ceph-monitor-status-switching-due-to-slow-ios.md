Title: Ceph monitor status switching due to slow IOs
Date: 2020-05-30
Tags: Ceph

I deployed a Ceph cluster (Nautilus, then upgraded to the Octopus
release) to store my personal data a few months ago. So far it has
been working pretty well, apart from a 1 hour partial outage that
won't be covered there, most probably linked to the issue described.

That said, I noticed that `mon.cephpi` was seen down for a few seconds
every few minutes, and that it happened during leader elections. And
when `mon.cephpi` goes back online, it seems triggers a new election a
few seconds after the previous one. (There `mon.cephpi` is also a bit
low on disk space, but that's not related to the issue under
examination).

```text
root@ceph-mon0:/var/log/ceph# zgrep ^2020-05-30T00:5 ceph.log.1.gz | egrep "INF|WRN"
2020-05-30T00:50:54.874314+0200 mon.yumy (mon.1) 26519 : cluster [INF] mon.yumy calling monitor election
2020-05-30T00:50:54.907529+0200 mon.ceph-mon0 (mon.0) 27086 : cluster [INF] mon.ceph-mon0 calling monitor election
2020-05-30T00:50:59.916206+0200 mon.ceph-mon0 (mon.0) 27087 : cluster [INF] mon.ceph-mon0 is new leader, mons ceph-mon0,yumy in quorum (ranks 0,1)
2020-05-30T00:51:00.026583+0200 mon.ceph-mon0 (mon.0) 27092 : cluster [WRN] Health check failed: 1/3 mons down, quorum ceph-mon0,yumy (MON_DOWN)
2020-05-30T00:51:00.026770+0200 mon.ceph-mon0 (mon.0) 27093 : cluster [INF] Health check cleared: MON_DISK_LOW (was: mon cephpi is low on available space)
2020-05-30T00:51:00.129247+0200 mon.ceph-mon0 (mon.0) 27094 : cluster [WRN] overall HEALTH_WARN 1/3 mons down, quorum ceph-mon0,yumy
2020-05-30T00:51:06.174123+0200 mon.cephpi (mon.2) 250 : cluster [INF] mon.cephpi calling monitor election
2020-05-30T00:51:06.239131+0200 mon.yumy (mon.1) 26520 : cluster [INF] mon.yumy calling monitor election
2020-05-30T00:51:06.240313+0200 mon.ceph-mon0 (mon.0) 27102 : cluster [INF] mon.ceph-mon0 calling monitor election
2020-05-30T00:51:06.286552+0200 mon.ceph-mon0 (mon.0) 27103 : cluster [INF] mon.ceph-mon0 is new leader, mons ceph-mon0,yumy,cephpi in quorum (ranks 0,1,2)
2020-05-30T00:51:06.403610+0200 mon.ceph-mon0 (mon.0) 27108 : cluster [INF] Health check cleared: MON_DOWN (was: 1/3 mons down, quorum ceph-mon0,yumy)
2020-05-30T00:51:06.403837+0200 mon.ceph-mon0 (mon.0) 27109 : cluster [INF] Cluster is now healthy
2020-05-30T00:51:06.517425+0200 mon.ceph-mon0 (mon.0) 27110 : cluster [INF] overall HEALTH_OK
2020-05-30T00:51:11.180148+0200 mon.ceph-mon0 (mon.0) 27116 : cluster [WRN] Health check failed: mon cephpi is low on available space (MON_DISK_LOW)
2020-05-30T00:52:42.757032+0200 mon.cephpi (mon.2) 251 : cluster [INF] mon.cephpi calling monitor election
2020-05-30T00:52:42.847724+0200 mon.ceph-mon0 (mon.0) 27203 : cluster [INF] mon.ceph-mon0 calling monitor election
2020-05-30T00:52:42.867228+0200 mon.yumy (mon.1) 26521 : cluster [INF] mon.yumy calling monitor election
2020-05-30T00:52:42.932928+0200 mon.ceph-mon0 (mon.0) 27204 : cluster [INF] mon.ceph-mon0 is new leader, mons ceph-mon0,yumy,cephpi in quorum (ranks 0,1,2)
2020-05-30T00:52:43.223146+0200 mon.ceph-mon0 (mon.0) 27210 : cluster [WRN] overall HEALTH_WARN mon cephpi is low on available space
2020-05-30T00:56:46.567727+0200 mon.yumy (mon.1) 26522 : cluster [INF] mon.yumy calling monitor election
2020-05-30T00:56:46.589153+0200 mon.ceph-mon0 (mon.0) 27448 : cluster [INF] mon.ceph-mon0 calling monitor election
2020-05-30T00:56:51.599236+0200 mon.ceph-mon0 (mon.0) 27449 : cluster [INF] mon.ceph-mon0 is new leader, mons ceph-mon0,yumy in quorum (ranks 0,1)
2020-05-30T00:56:51.700268+0200 mon.ceph-mon0 (mon.0) 27454 : cluster [WRN] Health check failed: 1/3 mons down, quorum ceph-mon0,yumy (MON_DOWN)
2020-05-30T00:56:51.700470+0200 mon.ceph-mon0 (mon.0) 27455 : cluster [INF] Health check cleared: MON_DISK_LOW (was: mon cephpi is low on available space)
2020-05-30T00:56:51.801453+0200 mon.ceph-mon0 (mon.0) 27456 : cluster [WRN] overall HEALTH_WARN 1/3 mons down, quorum ceph-mon0,yumy
2020-05-30T00:57:04.048894+0200 mon.ceph-mon0 (mon.0) 27469 : cluster [INF] mon.ceph-mon0 calling monitor election
2020-05-30T00:57:04.060391+0200 mon.yumy (mon.1) 26523 : cluster [INF] mon.yumy calling monitor election
2020-05-30T00:57:04.135749+0200 mon.ceph-mon0 (mon.0) 27470 : cluster [INF] mon.ceph-mon0 is new leader, mons ceph-mon0,yumy,cephpi in quorum (ranks 0,1,2)
2020-05-30T00:57:04.322415+0200 mon.ceph-mon0 (mon.0) 27476 : cluster [INF] Health check cleared: MON_DOWN (was: 1/3 mons down, quorum ceph-mon0,yumy)
2020-05-30T00:57:04.322579+0200 mon.ceph-mon0 (mon.0) 27477 : cluster [INF] Cluster is now healthy
2020-05-30T00:57:05.149468+0200 mon.ceph-mon0 (mon.0) 27478 : cluster [INF] overall HEALTH_OK
2020-05-30T00:57:08.912387+0200 mon.ceph-mon0 (mon.0) 27483 : cluster [WRN] Health check failed: mon cephpi is low on available space (MON_DISK_LOW)
```

Sometimes, I was also seeing `check_auth_rotating possible clock skew,
rotating keys expired way too early` messages in the logs of
non-monitor daemons (MDS, managers or OSD alike).

```text
root@cephpi:/var/log/ceph# zgrep 'clock skew' ceph-osd.0.log.1.gz 
2020-05-30T00:56:56.553+0200 ffff9d732bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:56:56.555279+0200)
2020-05-30T00:56:56.553+0200 ffff9e734bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:56:56.556551+0200)
2020-05-30T00:56:57.553+0200 ffff9d732bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:56:57.555610+0200)
2020-05-30T00:56:57.553+0200 ffff9e734bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:56:57.556922+0200)
2020-05-30T00:56:58.553+0200 ffff9d732bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:56:58.555918+0200)
2020-05-30T00:56:58.553+0200 ffff9e734bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:56:58.557175+0200)
2020-05-30T00:56:59.553+0200 ffff9d732bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:56:59.556250+0200)
2020-05-30T00:56:59.553+0200 ffff9e734bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:56:59.557567+0200)
2020-05-30T00:57:00.553+0200 ffff9d732bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:57:00.556559+0200)
2020-05-30T00:57:00.553+0200 ffff9e734bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:57:00.557819+0200)
2020-05-30T00:57:01.553+0200 ffff9d732bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:57:01.556899+0200)
2020-05-30T00:57:01.553+0200 ffff9e734bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:57:01.558013+0200)
2020-05-30T00:57:02.553+0200 ffff9d732bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:57:02.557226+0200)
2020-05-30T00:57:02.553+0200 ffff9e734bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:57:02.558396+0200)
2020-05-30T00:57:03.553+0200 ffff9d732bc0 -1 monclient: _check_auth_rotating possible clock skew, rotating keys expired way too early (before 2020-05-29T23:57:03.557531+0200)
```

Let's focus on the time period between `2020-05-30T00:56:51` and
`2020-05-30T00:57:04`, i.e 00:56:51 and 00:57:04. Here's my assumption
about what happened:

* At 00:56:51 `mon.cephpi` was seen down by `mon.ceph-mon0`
  
* between 00:56:56 and 00:57:03 `ceph-osd@0` obtained expired keys
  when trying to rotate them.

* At 00:57:04 `mon.cephpi` was seen up by `mon.ceph-mon0` and
  `ceph-osd@0` could rotate its keys succesfully.

It looks like between 00:56:51 and 00:57:04 `mon.cephpi` was out of
the quorum for 13 seconds and kept issuing expired keys to
`ceph-osd@0` during that period.


Let's have a look at the logs of `mon.cephpi`:

* Between 00:56:35 and 00:56:57, `mon.cephpi` was apparently writing
  to its rocksdb database, and it took 22 seconds to write 49442280
  bytes (i.e 50MB). This is why it missed the leader election that
  happened between 00:56:46 and 00:56:51, which resulted in
  `mon.cephpi` being flagged at down by the leader.

* At 00:56:57, when going back online, `mon.cephpi` triggered a new
  election, which ended at 00:57:04, with `mon.cephpi` being back in
  the monitors quorum, and able to issue valid keys again.

```text
2020-05-30T00:56:35.549+0200 ffffad98b400  4 rocksdb: [db/compaction_job.cc:1649] [default] Compaction start summary: Base version 1187 Base level 0, inputs: [48626(8490KB)], [48624(43MB)]
2020-05-30T00:56:35.549+0200 ffffad98b400  4 rocksdb: EVENT_LOG_v1 {"time_micros": 1590792995552781, "job": 1188, "event": "compaction_started", "compaction_reason": "ManualCompaction", "files_L0": [48626], "files_L6": [48624], "score": -1, "input_data_size": 53833362}
2020-05-30T00:56:57.853+0200 ffffad98b400  4 rocksdb: [db/compaction_job.cc:1332] [default] [JOB 1188] Generated table #48627: 4687 keys, 49442280 bytes
2020-05-30T00:56:57.853+0200 ffffad98b400  4 rocksdb: EVENT_LOG_v1 {"time_micros": 1590793017855925, "cf_name": "default", "job": 1188, "event": "table_file_creation", "file_number": 48627, "file_size": 49442280, "table_properties": {"data_size": 49336024, "index_size": 93526, "filter_size": 11909, "raw_key_size": 97594, "raw_average_key_size": 20, "raw_value_size": 49203175, "raw_average_value_size": 10497, "num_data_blocks": 2720, "num_entries": 4687, "filter_policy_name": "rocksdb.BuiltinBloomFilter"}}
2020-05-30T00:56:57.905+0200 ffffa797f400  1 mon.cephpi@2(electing) e14 collect_metadata :  no unique device id for : fallback method has no model nor serial'
2020-05-30T00:56:57.905+0200 ffffad98b400  4 rocksdb: [db/compaction_job.cc:1395] [default] [JOB 1188] Compacted 1@0 + 1@6 files to L6 => 49442280 bytes
2020-05-30T00:56:58.001+0200 ffffad98b400  4 rocksdb: (Original Log Time 2020/05/30-00:56:58.003695) [db/compaction_job.cc:768] [default] compacted to: base level 6 level multiplier 10.00 max bytes base 268435456 files[0 0 0 0 0 0 1] max score 0.00, MB/sec: 2.4 rd, 2.2 wr, level 6, files in(1, 1) out(1) MB in(8.3, 43.0) out(47.2), read-write-amplify(11.9) write-amplify(5.7) OK, records in: 5202, records dropped: 515 output_compression: NoCompression
2020-05-30T00:56:58.001+0200 ffffad98b400  4 rocksdb: (Original Log Time 2020/05/30-00:56:58.003819) EVENT_LOG_v1 {"time_micros": 1590793018003758, "job": 1188, "event": "compaction_finished", "compaction_time_micros": 22303522, "compaction_time_cpu_micros": 1184121, "output_level": 6, "num_output_files": 1, "total_output_size": 49442280, "num_input_records": 5202, "num_output_records": 4687, "num_subcompactions": 1, "output_compression": "NoCompression", "num_single_delete_mismatches": 0, "num_single_delete_fallthrough": 0, "lsm_state": [0, 0, 0, 0, 0, 0, 1]}
2020-05-30T00:56:58.005+0200 ffffad98b400  4 rocksdb: EVENT_LOG_v1 {"time_micros": 1590793018011605, "job": 1188, "event": "table_file_deletion", "file_number": 48626}
2020-05-30T00:56:58.021+0200 ffffad98b400  4 rocksdb: EVENT_LOG_v1 {"time_micros": 1590793018027883, "job": 1188, "event": "table_file_deletion", "file_number": 48624}
2020-05-30T00:56:58.025+0200 ffffa3176400  4 rocksdb: [db/db_impl_compaction_flush.cc:1403] [default] Manual compaction starting
2020-05-30T00:56:58.025+0200 ffffa3176400  4 rocksdb: [db/db_impl_compaction_flush.cc:1403] [default] Manual compaction starting
2020-05-30T00:56:58.025+0200 ffffa3176400  4 rocksdb: [db/db_impl_compaction_flush.cc:1403] [default] Manual compaction starting
2020-05-30T00:56:58.025+0200 ffffa3176400  4 rocksdb: [db/db_impl_compaction_flush.cc:1403] [default] Manual compaction starting
2020-05-30T00:56:58.025+0200 ffffa3176400  4 rocksdb: [db/db_impl_compaction_flush.cc:1403] [default] Manual compaction starting
2020-05-30T00:57:03.905+0200 ffffaa184400  1 paxos.2).electionLogic(33771) init, last seen epoch 33771, mid-election, bumping
2020-05-30T00:57:04.045+0200 ffffaa184400  1 mon.cephpi@2(electing) e14 collect_metadata :  no unique device id for : fallback method has no model nor serial'
2020-05-30T00:57:04.125+0200 ffffa797f400  1 mon.cephpi@2(electing) e14 collect_metadata :  no unique device id for : fallback method has no model nor serial'
2020-05-30T00:57:07.905+0200 ffffaa184400  1 mon.cephpi@2(peon).osd e4911 _set_new_cache_sizes cache_size:1020054731 inc_alloc: 71303168 full_alloc: 71303168 kv_alloc: 876609536
```

Let's do a quick check to see if how long it takes for cephpi to write
on the monitor's partition:

```text
root@cephpi:~# time sh -c "dd if=/dev/zero of=test bs=1M count=50; sync"
50+0 records in
50+0 records out
52428800 bytes (52 MB, 50 MiB) copied, 9.84231 s, 5.3 MB/s

real    0m10.375s
user    0m0.001s
sys     0m0.290s
```

Indeed, it takes `cephpi` 10 seconds to write 50MB of zeros. Which
makes sense because it is a Raspberry Pi with a MicroSD card used to
store the monitor's database. On the other hand writing 50MB to a
standard spinning disk takes less than 2 seconds:

```text
svc@yumy:/tmp$ time sh -c "dd if=/dev/zero of=test bs=1M count=50; sync"
50+0 records in
50+0 records out
52428800 bytes (52 MB, 50 MiB) copied, 0.111206 s, 471 MB/s

real	0m1.492s
user	0m0.003s
sys	0m0.117s
```

## Resolution

I eventually plugged a USB disk on `cephpi` to store `mon.cephpi`
data. It has been running for a few hour now, without any `MON_DOWN`
event, nor any leader election triggered.

In conclusion, one should avoid using slow storage devices (i.e SD
cards or USB sticks) to store Ceph monitors data. Monitors need to
write chunks of data (of 50MB in this case) at regular intervals in
less than a few seconds (less than 5 seconds I guess); otherwise, they
end up switching in and out of the monitors quorum and triggering many
elections.
