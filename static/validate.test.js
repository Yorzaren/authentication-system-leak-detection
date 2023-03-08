// This is a unit test file used by qunit for javascript functional testing
// The output of the test can be found in /tests/qunit_test.html

/* 
QUnit.module('NAME', function() {
	...
	
	QUnit.test('describe', function(assert) {
		assert.equal(fn, false);
	});
	
	
});
*/

QUnit.module('LengthCheck(string, min, max)', function() {
	QUnit.test('A string that meets the min requirements', function(assert) {
		assert.equal(LengthCheck("Hello", 5, 6), true);
	});
	QUnit.test('A string that meets the max requirements', function(assert) {
		assert.equal(LengthCheck("Hello!", 5, 6), true);
	});
	QUnit.test('A string that does not meet the requirements', function(assert) {
		assert.equal(LengthCheck("Hello!!", 5, 6), false);
	});
	QUnit.test('A string that does meet the requirements', function(assert) {
		assert.equal(LengthCheck("Hi person", 5, 10), true);
	});
	QUnit.test('A strange looking string that meets the a different set of requirements', function(assert) {
		assert.equal(LengthCheck("This!is#A&String*", 12, 32), true);
	});
});

QUnit.module('UppercaseCheck(string, min_number)', function() {
	QUnit.test('A string that meets the min requirements', function(assert) {
		assert.equal(UppercaseCheck("String", 1), true);
	});
	QUnit.test('A string that does not meet the requirements', function(assert) {
		assert.equal(UppercaseCheck("String", 7), false);
	});
	QUnit.test('A string that more than meets the requirements', function(assert) {
		assert.equal(UppercaseCheck("HELLOWoRdTeSTIng'", 5), true);
	});
	QUnit.test('A strange looking string that meets the a different set of requirements', function(assert) {
		assert.equal(UppercaseCheck("This!is#A&String*", 3), true);
	});
});

QUnit.module('LowercaseCheck(string, min_number)', function() {
	QUnit.test('A string meets the min requirements', function(assert) {
		assert.equal(LowercaseCheck("String", 5), true);
	});
	QUnit.test('A string that does not meet requirements', function(assert) {
		assert.equal(LowercaseCheck("HELLOWoRld", 5), false);
	});
	QUnit.test('A string that more than meets the requirements', function(assert) {
		assert.equal(LowercaseCheck("HELLOWoRdTeSTIngthisfunction'", 5), true);
	});
	QUnit.test('A strange looking string that meets the a different set of requirements', function(assert) {
		assert.equal(LowercaseCheck("This!is#A&String*", 3), true);
	});
});

QUnit.module('DigitCheck(string, min_number)', function() {
	QUnit.test('A string meets the min requirements', function(assert) {
		assert.equal(DigitCheck("Hello2", 1), true);
	});	
	QUnit.test('A string that does not meet requirements', function(assert) {
		assert.equal(DigitCheck("HELLOWoRld", 1), false);
	});
	QUnit.test('A string that more than meets the requirements', function(assert) {
		assert.equal(DigitCheck("123456", 5), true);
	});	
	QUnit.test('A strange looking string that meets the a different set of requirements', function(assert) {
		assert.equal(DigitCheck("This!7s#A&5tr1ng*", 3), true);
	});	
});

QUnit.module('SymbolCheck(string, min_number)', function() {
	QUnit.test('A string meets the min requirements', function(assert) {
		assert.equal(SymbolCheck("12##$dsc*&HJN", 5), true);
	});	
	QUnit.test('A string meets the min requirements because it has forbidden symbols that arent counted', function(assert) {
		assert.equal(SymbolCheck("1>2##$dsc*&HJN+_=", 5), true);
	});	
	QUnit.test('A string that doesnt meet requirements', function(assert) {
		assert.equal(SymbolCheck("asddsf23$%", 3), false);
	});	
	QUnit.test('A string that doesnt meet requirements because it has forbidden symbols that arent counted', function(assert) {
		assert.equal(SymbolCheck("a.s<d_dsf23", 1), false);
	});	
	QUnit.test('A strange looking string that meets the a different set of requirements', function(assert) {
		assert.equal(SymbolCheck("This!7s#A&5tr1ng*", 4), true);
	});	
});

QUnit.module('HasForbiddenCharCheck(string)', function() {
	QUnit.test('A string that is fine', function(assert) {
		assert.equal(HasForbiddenCharCheck("12##$dsc*&HJN"), false);
		assert.equal(HasForbiddenCharCheck("asddsf23$%"), false);
	});	
	QUnit.test('A string with forbidden symbols', function(assert) {
		assert.equal(HasForbiddenCharCheck("1>2##$dsc*&HJN+_="), true);
		assert.equal(HasForbiddenCharCheck("a.s<d_dsf23"), true);
	});	
	QUnit.test('A strange looking string with even more forbidden stuff', function(assert) {
		assert.equal(HasForbiddenCharCheck("heiß*我*π"), true);
	});	
});

QUnit.module('HasForbiddenUsernameCheck(string)', function() {
	QUnit.test('A string that is fine', function(assert) {
		assert.equal(HasForbiddenUsernameCheck("AUserName1"), false);
		assert.equal(HasForbiddenUsernameCheck("asddsf23"), false);
	});	
	QUnit.test('A string with forbidden symbols', function(assert) {
		assert.equal(HasForbiddenUsernameCheck("1>2##$dsc*&HJN+_="), true);
		assert.equal(HasForbiddenUsernameCheck("a.s<d_dsf23"), true);
		assert.equal(HasForbiddenUsernameCheck("12##$dsc*&HJN"), true);
	});	
	QUnit.test('A string empty string', function(assert) {
		assert.equal(HasForbiddenUsernameCheck(""), false); // Seem weird, we're only checking for bad characters not length
	});	
	QUnit.test('A strange looking string with even more forbidden stuff', function(assert) {
		assert.equal(HasForbiddenUsernameCheck("heiß*我*π"), true);
	});	
});

QUnit.module('HasMatchingStrings(string1, string2)', function() {	
	QUnit.test('Testing matching strings', function(assert) {
		assert.equal(HasMatchingStrings("asdf", "asdf"), true);
		assert.equal(HasMatchingStrings("@UJ#H821y34", "@UJ#H821y34"), true);
	});
	QUnit.test('Testing not matching strings', function(assert) {
		assert.equal(HasMatchingStrings("asd34riohjefui", "jsdkfh3uynu(&H@#MN?"), false);
	});
	
});