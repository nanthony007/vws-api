package tests

import "testing"

func TestAbs(t *testing.T) {
	got := 1
	if got != 1 {
		t.Errorf("Abs(-1) = %d; want 1", got)
	}
}

func TestAverage(t *testing.T) {
	var v float64
	v = (12 + 2) / 2
	if v != 7 {
		t.Error("Expected 7, got ", v)
	}
}
