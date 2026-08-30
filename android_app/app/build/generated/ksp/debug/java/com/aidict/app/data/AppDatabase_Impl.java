package com.aidict.app.data;

import androidx.annotation.NonNull;
import androidx.room.DatabaseConfiguration;
import androidx.room.InvalidationTracker;
import androidx.room.RoomDatabase;
import androidx.room.RoomOpenHelper;
import androidx.room.migration.AutoMigrationSpec;
import androidx.room.migration.Migration;
import androidx.room.util.DBUtil;
import androidx.room.util.TableInfo;
import androidx.sqlite.db.SupportSQLiteDatabase;
import androidx.sqlite.db.SupportSQLiteOpenHelper;
import com.aidict.app.data.dao.AppDao;
import com.aidict.app.data.dao.AppDao_Impl;
import java.lang.Class;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import javax.annotation.processing.Generated;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class AppDatabase_Impl extends AppDatabase {
  private volatile AppDao _appDao;

  @Override
  @NonNull
  protected SupportSQLiteOpenHelper createOpenHelper(@NonNull final DatabaseConfiguration config) {
    final SupportSQLiteOpenHelper.Callback _openCallback = new RoomOpenHelper(config, new RoomOpenHelper.Delegate(5) {
      @Override
      public void createAllTables(@NonNull final SupportSQLiteDatabase db) {
        db.execSQL("CREATE TABLE IF NOT EXISTS `profile` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `name` TEXT NOT NULL, `rank` INTEGER NOT NULL, `isDefault` INTEGER NOT NULL, `createdAt` INTEGER NOT NULL)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `app_setting` (`key` TEXT NOT NULL, `value` TEXT NOT NULL, PRIMARY KEY(`key`))");
        db.execSQL("CREATE TABLE IF NOT EXISTS `word` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `profileId` INTEGER NOT NULL, `term` TEXT NOT NULL, `language` TEXT, `lemma` TEXT, `color` TEXT, `stars` INTEGER NOT NULL, `searchCount` INTEGER NOT NULL, `sessionId` TEXT NOT NULL, `mode` TEXT NOT NULL, `createdAt` INTEGER NOT NULL, FOREIGN KEY(`profileId`) REFERENCES `profile`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE )");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_word_profileId` ON `word` (`profileId`)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `chat_message` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `wordId` INTEGER NOT NULL, `role` TEXT NOT NULL, `content` TEXT NOT NULL, `createdAt` INTEGER NOT NULL, FOREIGN KEY(`wordId`) REFERENCES `word`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE )");
        db.execSQL("CREATE INDEX IF NOT EXISTS `index_chat_message_wordId` ON `chat_message` (`wordId`)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `session` (`id` TEXT NOT NULL, `name` TEXT NOT NULL, `profileId` INTEGER NOT NULL, `createdAt` INTEGER NOT NULL, PRIMARY KEY(`id`))");
        db.execSQL("CREATE TABLE IF NOT EXISTS `note` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `title` TEXT NOT NULL, `content` TEXT NOT NULL, `createdAt` INTEGER NOT NULL)");
        db.execSQL("CREATE TABLE IF NOT EXISTS room_master_table (id INTEGER PRIMARY KEY,identity_hash TEXT)");
        db.execSQL("INSERT OR REPLACE INTO room_master_table (id,identity_hash) VALUES(42, '74610f53eb621dec06f43a4464306875')");
      }

      @Override
      public void dropAllTables(@NonNull final SupportSQLiteDatabase db) {
        db.execSQL("DROP TABLE IF EXISTS `profile`");
        db.execSQL("DROP TABLE IF EXISTS `app_setting`");
        db.execSQL("DROP TABLE IF EXISTS `word`");
        db.execSQL("DROP TABLE IF EXISTS `chat_message`");
        db.execSQL("DROP TABLE IF EXISTS `session`");
        db.execSQL("DROP TABLE IF EXISTS `note`");
        final List<? extends RoomDatabase.Callback> _callbacks = mCallbacks;
        if (_callbacks != null) {
          for (RoomDatabase.Callback _callback : _callbacks) {
            _callback.onDestructiveMigration(db);
          }
        }
      }

      @Override
      public void onCreate(@NonNull final SupportSQLiteDatabase db) {
        final List<? extends RoomDatabase.Callback> _callbacks = mCallbacks;
        if (_callbacks != null) {
          for (RoomDatabase.Callback _callback : _callbacks) {
            _callback.onCreate(db);
          }
        }
      }

      @Override
      public void onOpen(@NonNull final SupportSQLiteDatabase db) {
        mDatabase = db;
        db.execSQL("PRAGMA foreign_keys = ON");
        internalInitInvalidationTracker(db);
        final List<? extends RoomDatabase.Callback> _callbacks = mCallbacks;
        if (_callbacks != null) {
          for (RoomDatabase.Callback _callback : _callbacks) {
            _callback.onOpen(db);
          }
        }
      }

      @Override
      public void onPreMigrate(@NonNull final SupportSQLiteDatabase db) {
        DBUtil.dropFtsSyncTriggers(db);
      }

      @Override
      public void onPostMigrate(@NonNull final SupportSQLiteDatabase db) {
      }

      @Override
      @NonNull
      public RoomOpenHelper.ValidationResult onValidateSchema(
          @NonNull final SupportSQLiteDatabase db) {
        final HashMap<String, TableInfo.Column> _columnsProfile = new HashMap<String, TableInfo.Column>(5);
        _columnsProfile.put("id", new TableInfo.Column("id", "INTEGER", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsProfile.put("name", new TableInfo.Column("name", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsProfile.put("rank", new TableInfo.Column("rank", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsProfile.put("isDefault", new TableInfo.Column("isDefault", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsProfile.put("createdAt", new TableInfo.Column("createdAt", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysProfile = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesProfile = new HashSet<TableInfo.Index>(0);
        final TableInfo _infoProfile = new TableInfo("profile", _columnsProfile, _foreignKeysProfile, _indicesProfile);
        final TableInfo _existingProfile = TableInfo.read(db, "profile");
        if (!_infoProfile.equals(_existingProfile)) {
          return new RoomOpenHelper.ValidationResult(false, "profile(com.aidict.app.data.entities.Profile).\n"
                  + " Expected:\n" + _infoProfile + "\n"
                  + " Found:\n" + _existingProfile);
        }
        final HashMap<String, TableInfo.Column> _columnsAppSetting = new HashMap<String, TableInfo.Column>(2);
        _columnsAppSetting.put("key", new TableInfo.Column("key", "TEXT", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsAppSetting.put("value", new TableInfo.Column("value", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysAppSetting = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesAppSetting = new HashSet<TableInfo.Index>(0);
        final TableInfo _infoAppSetting = new TableInfo("app_setting", _columnsAppSetting, _foreignKeysAppSetting, _indicesAppSetting);
        final TableInfo _existingAppSetting = TableInfo.read(db, "app_setting");
        if (!_infoAppSetting.equals(_existingAppSetting)) {
          return new RoomOpenHelper.ValidationResult(false, "app_setting(com.aidict.app.data.entities.AppSetting).\n"
                  + " Expected:\n" + _infoAppSetting + "\n"
                  + " Found:\n" + _existingAppSetting);
        }
        final HashMap<String, TableInfo.Column> _columnsWord = new HashMap<String, TableInfo.Column>(11);
        _columnsWord.put("id", new TableInfo.Column("id", "INTEGER", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWord.put("profileId", new TableInfo.Column("profileId", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWord.put("term", new TableInfo.Column("term", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWord.put("language", new TableInfo.Column("language", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWord.put("lemma", new TableInfo.Column("lemma", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWord.put("color", new TableInfo.Column("color", "TEXT", false, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWord.put("stars", new TableInfo.Column("stars", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWord.put("searchCount", new TableInfo.Column("searchCount", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWord.put("sessionId", new TableInfo.Column("sessionId", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWord.put("mode", new TableInfo.Column("mode", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsWord.put("createdAt", new TableInfo.Column("createdAt", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysWord = new HashSet<TableInfo.ForeignKey>(1);
        _foreignKeysWord.add(new TableInfo.ForeignKey("profile", "CASCADE", "NO ACTION", Arrays.asList("profileId"), Arrays.asList("id")));
        final HashSet<TableInfo.Index> _indicesWord = new HashSet<TableInfo.Index>(1);
        _indicesWord.add(new TableInfo.Index("index_word_profileId", false, Arrays.asList("profileId"), Arrays.asList("ASC")));
        final TableInfo _infoWord = new TableInfo("word", _columnsWord, _foreignKeysWord, _indicesWord);
        final TableInfo _existingWord = TableInfo.read(db, "word");
        if (!_infoWord.equals(_existingWord)) {
          return new RoomOpenHelper.ValidationResult(false, "word(com.aidict.app.data.entities.Word).\n"
                  + " Expected:\n" + _infoWord + "\n"
                  + " Found:\n" + _existingWord);
        }
        final HashMap<String, TableInfo.Column> _columnsChatMessage = new HashMap<String, TableInfo.Column>(5);
        _columnsChatMessage.put("id", new TableInfo.Column("id", "INTEGER", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsChatMessage.put("wordId", new TableInfo.Column("wordId", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsChatMessage.put("role", new TableInfo.Column("role", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsChatMessage.put("content", new TableInfo.Column("content", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsChatMessage.put("createdAt", new TableInfo.Column("createdAt", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysChatMessage = new HashSet<TableInfo.ForeignKey>(1);
        _foreignKeysChatMessage.add(new TableInfo.ForeignKey("word", "CASCADE", "NO ACTION", Arrays.asList("wordId"), Arrays.asList("id")));
        final HashSet<TableInfo.Index> _indicesChatMessage = new HashSet<TableInfo.Index>(1);
        _indicesChatMessage.add(new TableInfo.Index("index_chat_message_wordId", false, Arrays.asList("wordId"), Arrays.asList("ASC")));
        final TableInfo _infoChatMessage = new TableInfo("chat_message", _columnsChatMessage, _foreignKeysChatMessage, _indicesChatMessage);
        final TableInfo _existingChatMessage = TableInfo.read(db, "chat_message");
        if (!_infoChatMessage.equals(_existingChatMessage)) {
          return new RoomOpenHelper.ValidationResult(false, "chat_message(com.aidict.app.data.entities.ChatMessage).\n"
                  + " Expected:\n" + _infoChatMessage + "\n"
                  + " Found:\n" + _existingChatMessage);
        }
        final HashMap<String, TableInfo.Column> _columnsSession = new HashMap<String, TableInfo.Column>(4);
        _columnsSession.put("id", new TableInfo.Column("id", "TEXT", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSession.put("name", new TableInfo.Column("name", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSession.put("profileId", new TableInfo.Column("profileId", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsSession.put("createdAt", new TableInfo.Column("createdAt", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysSession = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesSession = new HashSet<TableInfo.Index>(0);
        final TableInfo _infoSession = new TableInfo("session", _columnsSession, _foreignKeysSession, _indicesSession);
        final TableInfo _existingSession = TableInfo.read(db, "session");
        if (!_infoSession.equals(_existingSession)) {
          return new RoomOpenHelper.ValidationResult(false, "session(com.aidict.app.data.entities.Session).\n"
                  + " Expected:\n" + _infoSession + "\n"
                  + " Found:\n" + _existingSession);
        }
        final HashMap<String, TableInfo.Column> _columnsNote = new HashMap<String, TableInfo.Column>(4);
        _columnsNote.put("id", new TableInfo.Column("id", "INTEGER", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsNote.put("title", new TableInfo.Column("title", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsNote.put("content", new TableInfo.Column("content", "TEXT", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsNote.put("createdAt", new TableInfo.Column("createdAt", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysNote = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesNote = new HashSet<TableInfo.Index>(0);
        final TableInfo _infoNote = new TableInfo("note", _columnsNote, _foreignKeysNote, _indicesNote);
        final TableInfo _existingNote = TableInfo.read(db, "note");
        if (!_infoNote.equals(_existingNote)) {
          return new RoomOpenHelper.ValidationResult(false, "note(com.aidict.app.data.entities.Note).\n"
                  + " Expected:\n" + _infoNote + "\n"
                  + " Found:\n" + _existingNote);
        }
        return new RoomOpenHelper.ValidationResult(true, null);
      }
    }, "74610f53eb621dec06f43a4464306875", "4700cf2408a5cedb980812a29fb3d6ee");
    final SupportSQLiteOpenHelper.Configuration _sqliteConfig = SupportSQLiteOpenHelper.Configuration.builder(config.context).name(config.name).callback(_openCallback).build();
    final SupportSQLiteOpenHelper _helper = config.sqliteOpenHelperFactory.create(_sqliteConfig);
    return _helper;
  }

  @Override
  @NonNull
  protected InvalidationTracker createInvalidationTracker() {
    final HashMap<String, String> _shadowTablesMap = new HashMap<String, String>(0);
    final HashMap<String, Set<String>> _viewTables = new HashMap<String, Set<String>>(0);
    return new InvalidationTracker(this, _shadowTablesMap, _viewTables, "profile","app_setting","word","chat_message","session","note");
  }

  @Override
  public void clearAllTables() {
    super.assertNotMainThread();
    final SupportSQLiteDatabase _db = super.getOpenHelper().getWritableDatabase();
    final boolean _supportsDeferForeignKeys = android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP;
    try {
      if (!_supportsDeferForeignKeys) {
        _db.execSQL("PRAGMA foreign_keys = FALSE");
      }
      super.beginTransaction();
      if (_supportsDeferForeignKeys) {
        _db.execSQL("PRAGMA defer_foreign_keys = TRUE");
      }
      _db.execSQL("DELETE FROM `profile`");
      _db.execSQL("DELETE FROM `app_setting`");
      _db.execSQL("DELETE FROM `word`");
      _db.execSQL("DELETE FROM `chat_message`");
      _db.execSQL("DELETE FROM `session`");
      _db.execSQL("DELETE FROM `note`");
      super.setTransactionSuccessful();
    } finally {
      super.endTransaction();
      if (!_supportsDeferForeignKeys) {
        _db.execSQL("PRAGMA foreign_keys = TRUE");
      }
      _db.query("PRAGMA wal_checkpoint(FULL)").close();
      if (!_db.inTransaction()) {
        _db.execSQL("VACUUM");
      }
    }
  }

  @Override
  @NonNull
  protected Map<Class<?>, List<Class<?>>> getRequiredTypeConverters() {
    final HashMap<Class<?>, List<Class<?>>> _typeConvertersMap = new HashMap<Class<?>, List<Class<?>>>();
    _typeConvertersMap.put(AppDao.class, AppDao_Impl.getRequiredConverters());
    return _typeConvertersMap;
  }

  @Override
  @NonNull
  public Set<Class<? extends AutoMigrationSpec>> getRequiredAutoMigrationSpecs() {
    final HashSet<Class<? extends AutoMigrationSpec>> _autoMigrationSpecsSet = new HashSet<Class<? extends AutoMigrationSpec>>();
    return _autoMigrationSpecsSet;
  }

  @Override
  @NonNull
  public List<Migration> getAutoMigrations(
      @NonNull final Map<Class<? extends AutoMigrationSpec>, AutoMigrationSpec> autoMigrationSpecs) {
    final List<Migration> _autoMigrations = new ArrayList<Migration>();
    return _autoMigrations;
  }

  @Override
  public AppDao appDao() {
    if (_appDao != null) {
      return _appDao;
    } else {
      synchronized(this) {
        if(_appDao == null) {
          _appDao = new AppDao_Impl(this);
        }
        return _appDao;
      }
    }
  }
}
